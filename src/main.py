import logging
import sys

from ctrl import Ctrl

logging.basicConfig(level=logging.INFO,
                    filename='KnightReport.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

fperr = open("KnightReport.err", "w")
sys.stderr = fperr

version = "0.1.1"
website = "https://github.com/cutecutecat/KnightReport"

if __name__ == "__main__":
    logging.info("坎公骑冠剑————超级骑士报表————v{:s}".format(version))
    logging.info("by [ NGA | bigfun | TapTap ]@星星星痕")
    logging.info("如有疑问或建议可以到{:s}提交issue".format(website))
    tool = Ctrl()
    tool.exec()

    fperr.close()
