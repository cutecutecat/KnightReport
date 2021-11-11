import logging

from ctrl.ctrl import Ctrl


def initCtrl(cj):
    logging.info("开始数据检索流程")

    ctrl = Ctrl(cj)
    ctrl.exec()
