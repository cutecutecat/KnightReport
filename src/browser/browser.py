import json
import logging
import pickle
import sys
from http import cookiejar
from threading import Thread
from time import sleep

from requests import get
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
from requests.cookies import create_cookie
from requests.utils import dict_from_cookiejar

from config.constants import LoginURL, GuildStatusURL, Headers


class MainWindow(QMainWindow):
    valid = pyqtSignal(bool)

    def __init__(self, queue):
        super().__init__()

        self.loaded = False

        self.cookiesJar = None
        self.max_retry = 20
        self.queue = queue
        self.pickerStarted = False

        self.cookiesPicker = Thread(target=self.updateCookies)

        self.setWindowTitle('Login Browser')
        self.showMaximized()

        self.browser = QWebEngineView()
        self.browser.page().loadFinished.connect(self.checkLoaded)
        self.browser.page().contentsSizeChanged.connect(self.getwidth)
        self.valid.connect(super().closeEvent)

        self.browser.load(QUrl(LoginURL))
        self.setCentralWidget(self.browser)

    def closeEvent(self, closeEvent) -> None:
        super().closeEvent(closeEvent)

    def checkLoaded(self):
        if not self.pickerStarted:
            self.pickerStarted = True
            self.cookiesPicker.start()

    def updateCookies(self):
        tried = 0
        while self.cookiesJar is None:
            sleep(1)
            self.getCookiesByJs()
        while True:
            r = get(GuildStatusURL, cookies=self.cookiesJar, headers=Headers)
            code_status = json.loads(r.text)['code']
            if tried > self.max_retry:
                raise TimeoutError("超时{:d}s，未获得有效cookies".format(self.max_retry * 15))
            if code_status == 0:
                logging.info("cookies验证通过")
                self.queue.put(pickle.dumps([c for c in self.cookiesJar]), block=True)
                sys.exit()
            elif code_status == 401:
                logging.warning("cookies 无效, 请完成登录，等待15秒重试...")
                sleep(15)
                self.getCookiesByJs()
                tried += 1
                continue
            else:
                raise RuntimeError("未知的错误码 {:d}".format(code_status))

    def getwidth(self):
        def zoom(content_width: int):
            desktop_width = QApplication.desktop().width()
            self.browser.setZoomFactor(desktop_width // content_width - 0.5)

        runJs = '''
        function getWidth(){return document.getElementById('root').offsetWidth};
        getWidth();
        '''
        self.browser.page().runJavaScript(runJs, zoom)

    def getCookiesByJs(self):
        runJs = '''
        function getCookie(){return document.cookie};
        getCookie();
        '''
        self.browser.page().runJavaScript(runJs, self.collect)

    def collect(self, cookies_raw: str):
        cookies = cookies_raw.split('; ')
        self.cookiesJar = cookiejar.CookieJar()
        for cookie_str in cookies:
            name, value = cookie_str.split('=')
            self.cookiesJar.set_cookie(create_cookie(name, value, domain=".bigfun.cn"))
        logging.info(f"尝试读取cookies, 有效key{tuple(dict_from_cookiejar(self.cookiesJar).keys())}")
