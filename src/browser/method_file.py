from http import cookiejar
from requests.cookies import create_cookie  # type: ignore


class MethodFile:
    def __init__(self):
        with open('cookies.txt', 'r') as f:
            self.cookies_raw = f.read()

    def fetch_cookies(self):
        cookies = self.cookies_raw.strip(' \'') \
            .rstrip(' \'').replace(' ', '').split(';')
        cj = cookiejar.CookieJar()
        for cookie in cookies:
            name, value = cookie.split('=')
            cj.set_cookie(create_cookie(name, value, domain='.bigfun.cn'))
        return cj
