import json
import os.path
from pathlib import Path
from urllib.parse import quote

import requests

from utils.LoginDataItem import LoginDataItem

url_of_host = "https://hitfile.net"


def _login(login: str = "marozalex@gmail.com", password: str = "069024097ff"):
    _url = url_of_host + "/user/login"

    payload = (
        'page_referrer='
        f'&user[login]={login}'
        f'&user[pass]={password}'
        '&user[submit]=Вход'
        '&user[memory]=on'
    )

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(_url, headers=headers, data=payload)

    return {
        "kohanasession7": response.cookies.get("kohanasession7")
    }

def login_and_save_cookies(_path_to_login_file: Path):
    login_data: LoginDataItem = LoginDataItem.from_raw(open(_path_to_login_file).read())
    _path_to_login_cookies_file = _path_to_login_file.with_name(f"{login_data.login}_cookies.json")

    cookies = _login(login_data.login, login_data.password)

    with open(_path_to_login_cookies_file, "w+") as cookies_file:
        cookies_file.write(json.dumps(cookies))

def _get_cookies(_path_to_login_file: Path) -> str:
    with open(_path_to_login_file) as login_file: login_data: LoginDataItem = LoginDataItem.from_raw(login_file.read())
    _path_to_login_cookies_file = _path_to_login_file.with_name(f"{login_data.login}_cookies.json")
    cookies = ""

    if os.path.exists(_path_to_login_cookies_file):
        with open(_path_to_login_cookies_file) as cookies_file:
            cookies_raw = json.loads(cookies_file.read())
            cookies = "".join([f"{cookie}={cookies_raw[cookie]};" for cookie in cookies_raw])

    return cookies

# todo: maybe move to another func or refactor
def is_cookies_expired(_cookies: str):
    from lxml.html import fromstring

    res = requests.get(
        url_of_host,
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            "Cookie": _cookies
        }
    )

    tree = fromstring(res.text)
    element = tree.xpath("//*[@class='panel-login-sub']/*[@class='user']")
    return False if len(element) == 1 else True

def get_cookies(_path_to_login_file: Path) -> str:
    _cookies = _get_cookies(_path_to_login_file)

    if is_cookies_expired(_cookies):
        login_and_save_cookies(_path_to_login_file)
        _cookies = _get_cookies(_path_to_login_file)

    return _cookies


def get_headers_of_account_with_auth(_path_to_login_file: Path) -> dict:
    cookies = get_cookies(_path_to_login_file)

    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        "Cookie": cookies
    }


def get_path_to_login_file() -> Path:
    _path_to_login_file_from_env = os.environ.get("PATH_TO_LOGIN_FILE")
    return Path(_path_to_login_file_from_env)