import logging
import multiprocessing
import sys

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

if __name__ == "__main__":
    cj = initBrowser()
    ctrl = initCtrl(cj)
