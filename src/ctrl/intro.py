import logging
import pickle
from http import cookiejar

from ctrl.ctrl import Ctrl


def initCtrl(queue):
    logging.info("开始数据检索流程")
    cookies = pickle.loads(queue.get())
    cookiesJar = cookiejar.CookieJar()
    for cookie in cookies:
        cookiesJar.set_cookie(cookie)

    ctrl = Ctrl(cookiesJar)
    ctrl.exec()
