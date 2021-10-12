import logging
import multiprocessing
import sys
from multiprocessing import Process, set_start_method, Queue, freeze_support, active_children, parent_process
from time import sleep

from browser.intro import initBrowser
from ctrl.intro import initCtrl

fperr = open("KnightReport.err.log", "a")
sys.stderr = fperr

logging.basicConfig(level=logging.INFO,
                    filename='KnightReport.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

if multiprocessing.current_process().name == 'MainProcess':
    version = "0.1.2"
    website = "https://github.com/cutecutecat/KnightReport"

    logging.info("坎公骑冠剑————超级骑士报表————v{:s}".format(version))
    logging.info("by [ NGA | bigfun | TapTap ]@星星星痕")
    logging.info("如有疑问或建议可以到{:s}提交issue".format(website))


def excepthook(exctype, value, traceback):
    for p in active_children():
        p.terminate()
    sys.__excepthook__(exctype, value, traceback)


if __name__ == "__main__":
    # Add support for when a program which uses multiprocessing
    # has been frozen to produce a Windows executable.
    freeze_support()
    set_start_method('spawn')
    queue = Queue(1)
    sys.excepthook = excepthook

    browser = Process(target=initBrowser, args=(queue,))
    browser.start()

    while queue.empty():
        if not browser.is_alive():
            raise RuntimeError('浏览器被用户关闭')
        sleep(3)
    browser.terminate()

    ctrl = Process(target=initCtrl, args=(queue,))
    ctrl.start()
    ctrl.join()
