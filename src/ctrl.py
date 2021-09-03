import json
import logging
import webbrowser
from os import path
from http.cookiejar import CookieJar
from time import sleep
from typing import Dict, Sequence, Set, Union

import browser_cookie3
import requests

import constants
from utils import Info, Combat


def user_login():
    """
    ask user to login for fetch cookies(strictly use Windows Edge)
    :return:
    """
    ctrl = webbrowser.get(using='edge')
    ctrl.open(constants.LoginURL)


class Ctrl:
    def __init__(self):
        self.max_retry = 20

        self.cookiesJar: Union[CookieJar, None] = None

        self.dates: Sequence[str] = list()
        self.uid_name: Dict[int, str] = dict()
        self.person_info: Dict[int, Info] = dict()
        self.combat: Union[Combat, None] = None
        self.all_uid: Set = set()



    def exec(self):
        r"""
        execute the whole generating stream
        """
        user_login()
        try:
            guild_status = self.get_guild()
            self.extract_guild_info(guild_status)

            for i, date in enumerate(self.dates):
                attack_status = self.get_date(date)
                self.extract_date_info(i, attack_status)
            self.combat.marshal(self.person_info.values(), "./report.csv")
            logging.info("会战数据已写入报表 -> {:s}".format(path.abspath("./report.csv")))
            logging.info("可以使用Excel或WPS等软件打开csv文件")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("网络故障")
        except ValueError:
            raise RuntimeError("请关闭代理")

    def get_guild(self) -> Dict:
        r"""
        send network requests and get guild status
        """
        tried = 0
        while True:
            cj = browser_cookie3.edge(domain_name=".bigfun.cn")
            r = requests.get(constants.GuildStatusURL, cookies=cj, headers=constants.Headers)
            guild_status = json.loads(r.text)
            if tried > self.max_retry:
                raise TimeoutError("超时{:d}s，未获得有效cookies".format(self.max_retry * 15))
            if guild_status['code'] == 0:
                logging.info("成功读取公会数据")
                self.cookiesJar = cj
                return guild_status
            elif guild_status['code'] == 401:
                logging.warning("cookies 未正确获取, 请完成登录，等待15秒重试...")
                sleep(15)
                tried += 1
                continue
            else:
                raise RuntimeError("未知的错误码 {:d}".format(guild_status['code']))

    def extract_guild_info(self, guild_status: Dict):
        r"""
        extract info from guild json data according colleagues and dates
        """
        colleagues = guild_status['data']['member']
        self.dates = guild_status['data']['date']
        self.uid_name = {person['id']: person['name'] for person in colleagues}
        self.person_info = {uid: Info(uid, name, len(self.dates)) for uid, name in self.uid_name.items()}
        self.combat = Combat(self.dates)
        self.all_uid = set(self.uid_name.keys())

    def get_date(self, date: str) -> Dict:
        r"""
        send network requests and get combat status of the day
        """
        url = constants.DateStatusURL.format(date)
        r = requests.get(url, cookies=self.cookiesJar, headers=constants.Headers)
        attack_status = json.loads(r.text)
        if attack_status['code'] != 0:
            raise RuntimeError("未知的错误码 {:d}".format(attack_status['code']))
        else:
            logging.info("成功读取{:s}会战数据".format(date))
        return attack_status

    def extract_date_info(self, index: int, attack_status: Dict):
        r"""
        extract info from guild json data according combat of a day
        """
        uid_today = set()
        # People join combat today
        for person_attack in attack_status['data']:
            uid = person_attack['user_id']
            if uid not in uid_today:
                uid_today.add(uid)
            else:
                logging.warning(f"重复玩家uid {uid}, 已去除")
                continue

            hits = person_attack['damage_num']
            # check abnormal hits today
            if hits > 3:
                logging.warning("玩家uid{:d}于日期{:s}对boss{:s}异常出刀数{:d}"
                                .format(uid, self.dates[index], boss_name,
                                        self.person_info[uid].boss_hits[boss_name]))
                logging.warning("记录当日战斗日志")
                logging.warning(f"{json.dumps(attack_status)}")
            damage = person_attack['damage_total']
            self.person_info[uid].hits += hits
            self.person_info[uid].damage += damage
            self.person_info[uid].omission[index] = hits - 3

            damage_list = person_attack['damage_list']
            for damage_once in damage_list:
                boss_name = damage_once['boss_name']
                self.combat.add_boss(boss_name)
                damage = damage_once['damage']
                self.person_info[uid].add_hit(boss_name, damage)
        # People don't join combat today
        for uid in self.all_uid.difference(uid_today):
            self.person_info[uid].omission[index] = -3
