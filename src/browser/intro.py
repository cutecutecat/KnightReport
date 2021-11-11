import logging
from os.path import exists
from browser.method_auto import MethodAuto
from browser.method_file import MethodFile


def initBrowser():
    logging.info("开始尝试，获得用户cookies")
    # 如果当前目录下存在cookies.txt，从其中读取cookies
    # 否则，尝试自动获取cookies
    if exists('cookies.txt'):
        logging.info("当前路径下发现cookies.txt，尝试从文件中获得cookies")
        method = MethodFile()
        try:
            cj = method.fetch_cookies()
            return cj
        except:
            logging.warning("cookies.txt解析失败，请检查文件内容")
    method = MethodAuto()
    cj = method.fetch_cookies()
    return cj
