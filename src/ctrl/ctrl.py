import json
import logging
from os.path import abspath
from http.cookiejar import CookieJar
from typing import Dict, Sequence, Set, Union

import requests

from config.constants import GuildStatusURL, DateStatusURL, Headers
from ctrl.utils import Info, Combat


class Ctrl:
    def __init__(self, cj):
        self.cookiesJar: CookieJar = cj

        self.dates: Sequence[str] = list()
        self.uid_name: Dict[int, str] = dict()
        self.person_info: Dict[int, Info] = dict()
        self.combat: Union[Combat, None] = None
        self.all_uid: Set = set()

    def exec(self):
        r"""
        execute the whole generating stream
        """
        try:
            guild_status = self.get_guild()
            self.extract_guild_info(guild_status)

            for i, date in enumerate(self.dates):
                attack_status = self.get_date(date)
                self.extract_date_info(i, attack_status)
            self.combat.marshal(self.person_info.values(), "./report.csv")
            logging.info("会战数据已写入报表 -> {:s}".format(abspath("./report.csv")))
            logging.info("可以使用Excel或WPS等软件打开csv文件")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("网络故障")
        except ValueError:
            raise RuntimeError("请关闭代理")

    def get_guild(self) -> Dict:
        r"""
        send network requests and get guild status
        """
        url = GuildStatusURL
        r = requests.get(url, cookies=self.cookiesJar, headers=Headers)
        guild_status = json.loads(r.text)
        if guild_status['code'] == 0:
            logging.info("成功读取公会数据")
            return guild_status
        elif guild_status['code'] == 401:
            logging.error("cookies 失效, 请再次尝试，多次出现请进行反馈")
            raise RuntimeError("cookies 失效, 请再次尝试，多次出现请进行反馈")
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
        url = DateStatusURL.format(date)
        r = requests.get(url, cookies=self.cookiesJar, headers=Headers)
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
            if hits > 3 and self.person_info[uid].omission[index - 1] < 0:
                logging.warning("玩家uid {:d}于日期{:s} 额外跨日出刀{:d}，成功迁移到前一天"
                                .format(uid, self.dates[index], hits - 3))
                self.person_info[uid].omission[index - 1] += (hits - 3)
                hits -= 3
            elif hits > 3:
                logging.warning("玩家uid {:d}于日期{:s} 异常出刀数{:d}"
                                .format(uid, self.dates[index], hits))
                logging.warning("记录当日战斗日志")
                logging.warning(attack_status)
            damage = person_attack['damage_total']
            self.person_info[uid].hits += hits
            self.person_info[uid].damage += damage
            self.person_info[uid].omission[index] = hits - 3

            damage_list = person_attack['damage_list']
            for damage_once in damage_list:
                boss_name = damage_once['boss_name']
                self.combat.add_boss(boss_name)
                damage = damage_once['damage']
                killed = damage_once['is_kill']
                if killed != 0 and killed != 1:
                    logging.error("玩家uid {:d}于日期{:s} 异常尾刀{:d}"
                                  .format(uid, self.dates[index], killed))
                    logging.error("记录当日战斗日志")
                    logging.error(attack_status)
                self.person_info[uid].add_hit(boss_name, damage, killed)
        # People don't join combat today
        for uid in self.all_uid.difference(uid_today):
            self.person_info[uid].omission[index] = -3
