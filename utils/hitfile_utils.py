from typing import NamedTuple

import requests
from httpx import request

from exceptions import AccountIsFreeException, DailyDownloadLimitExpiredException


class ArchiveDownloadMetadata(NamedTuple):
    link: str
    name: str
    size: str

def is_account_free(html_tree):
    premium_account_type_xpath = "//span//a[@href='/premium/info']"
    premium_account_type_search_result = html_tree.xpath(premium_account_type_xpath)
    return False if len(premium_account_type_search_result) == 1 else True

def is_daily_download_limit_expired(html_tree):
    download_limit_message_xpath = "//div[@id='unread-messages-block'] | //div[@class='panel-round error']"
    download_limit_message_search_result = html_tree.xpath(download_limit_message_xpath)
    return True if len(download_limit_message_search_result) == 1 else False


def validate_hitfile_tree(html_tree):
    if is_account_free(html_tree): raise AccountIsFreeException("The account is free")
    if is_daily_download_limit_expired(html_tree): raise DailyDownloadLimitExpiredException("Daily download limit is expired.")

def _request(url: str, headers: dict, validation: bool = True):
    from lxml.html import fromstring
    _archive_id: str = url.split("https://hitf.cc/")[1]
    _url = 'https://hitfile.net/{}'.format(_archive_id)
    # _url = requests.get(url).url

    res = requests.get(_url, headers=headers)
    html_tree = fromstring(res.text)
    if validation: validate_hitfile_tree(html_tree)
    return html_tree

def _get_size_of_archive(html_tree) -> str:
    archive_size_xpath = "//title[contains(text(), 'Download file')]/text()"
    size_element = html_tree.xpath(archive_size_xpath)
    size = size_element[0].split("(")[1].split(")")[0]
    return str(size)

def _get_download_url_of_archive(html_tree) -> str:
    archive_download_link_xpath = "//h1/a/@href"
    link_element = html_tree.xpath(archive_download_link_xpath)
    link = link_element[0]
    return str(link)

def _get_name_of_archive(html_tree) -> str:
    archive_name_xpath = "//meta[@name='keywords']/@content"
    name_element = html_tree.xpath(archive_name_xpath)
    name = name_element[0].strip().split(",  {},")[0]
    return str(name)

def get_download_url_of_archive(url: str, headers: dict) -> str:
    return _get_download_url_of_archive(_request(url, headers))

def get_size_of_archive(url: str, headers: dict) -> str:
    return _get_size_of_archive(_request(url, headers, validation=False))

def get_name_of_archive(url: str, headers: dict):
    return _get_name_of_archive(_request(url, headers, validation=False))

def get_archive_metadata(url: str, headers: dict) -> ArchiveDownloadMetadata:
    html_tree = _request(url, headers)
    return ArchiveDownloadMetadata(
        link=_get_download_url_of_archive(html_tree),
        name=_get_name_of_archive(html_tree),
        size=_get_size_of_archive(html_tree)
    )


