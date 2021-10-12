import logging
import sys

from PyQt5.QtWidgets import QApplication

from browser.browser import MainWindow


def initBrowser(queue):
    logging.info("启动浏览器进行登录，获得用户cookies")
    logging.info("登录完成后浏览器会自行关闭，请勿关闭窗口")
    app = QApplication(sys.argv)
    window = MainWindow(queue)
    window.show()
    app.exec()
