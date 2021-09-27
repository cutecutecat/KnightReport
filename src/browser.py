import logging
from http import cookiejar
from threading import Thread
from time import sleep

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from requests.cookies import create_cookie
from requests.utils import dict_from_cookiejar


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.loaded = False
        self.valid = False
        self.cj = None

        self.setWindowTitle('Login Browser')
        self.showMaximized()

        self.browser = QWebEngineView()
        self.browser.page().loadFinished.connect(self.checkLoaded)
        self.browser.page().contentsSizeChanged.connect(self.getwidth)

        self.browser.load(QUrl("https://www.bigfun.cn/tools/gt/"))
        self.setCentralWidget(self.browser)

        self.work = Thread(target=self.checkCookies)
        self.work.start()

    def checkLoaded(self):
        self.loaded = True

    def checkCookies(self):
        while not self.valid:
            while not self.loaded:
                sleep(1)
            self.getCookiesByJs()
            sleep(15)
        # self.close()

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
        self.cj = cookiejar.CookieJar()
        for cookie_str in cookies:
            name, value = cookie_str.split('=')
            self.cj.set_cookie(create_cookie(name, value, domain=".bigfun.cn"))
        logging.info(f"尝试读取cookies, 有效key{tuple(dict_from_cookiejar(self.cj).keys())}")
