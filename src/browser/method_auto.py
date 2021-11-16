import json
import logging
import sys
import webbrowser
from time import sleep

import browser_cookie3
import requests

from config.constants import LoginURL, EdgePath, Headers, GuildStatusURL


class MethodAuto:
    def __init__(self):
        self.maxTry = 10
        self.wait = 15

        if sys.platform == 'darwin':
            self.use = self.try_browser(['chrome'])
        elif sys.platform == 'win32':
            webbrowser.register('chrome', None,
                                webbrowser.GenericBrowser(
                                    ['powershell.exe', 'start chrome %s']))
            webbrowser.register('edge', None,
                                webbrowser.BackgroundBrowser(EdgePath))
            self.use = self.try_browser(['chrome', 'edge'])
        else:
            raise OSError("unsupported OS system")
        if len(self.use) == 0:
            raise RuntimeError("unable to find support browser")

    @staticmethod
    def try_browser(browser_list: list) -> str:
        use = ""
        for browser in browser_list:
            ctrl = webbrowser.get(using=browser)
            ret = ctrl.open(LoginURL)
            if ret:
                logging.info(f"成功启动{browser}浏览器")
                use = browser
            else:
                logging.warning(f"尝试启动{browser}浏览器失败")
                continue
        return use

    def _select_browser_cookies(self):
        if self.use == 'edge':
            return browser_cookie3.edge(domain_name=".bigfun.cn")
        elif self.use == 'chrome':
            return browser_cookie3.chrome(domain_name=".bigfun.cn")
        else:
            raise RuntimeError("unsupported browser")

    def fetch_cookies(self):
        tried = 0
        while True:
            if tried > self.maxTry:
                logging.error(f"超时 {self.wait * self.maxTry}s")
                raise RuntimeError(f"超时 {self.wait * self.maxTry}s")
            cj = self._select_browser_cookies()
            url = GuildStatusURL
            r = requests.get(url, cookies=cj, headers=Headers)
            guild_status = json.loads(r.text)
            if guild_status['code'] == 0:
                logging.info("cookies验证成功")
                return cj
            elif guild_status['code'] == 401:
                tried += 1
                logging.error("cookies验证失败，等待15s")
                sleep(self.wait)
                continue
            else:
                raise RuntimeError("未知的错误码 {:d}".format(guild_status['code']))
