import os
import uuid
from pathlib import Path
from typing import Literal

import httpx
import urllib3
import wget
from loguru import logger

from requests.adapters import HTTPAdapter
import ssl
import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed
from urllib3.util.retry import Retry



def _download_file_by_requests(url: str, path_to_save: Path | str, headers: dict[str, str] = None):
    with open(Path(path_to_save), "wb") as f:
        session = requests.Session()

        adapter = HTTPAdapter(max_retries=5)
        session.mount('https://', adapter)

        logger.debug(f"Making request to {url}")

        res = session.get(
            url,
            headers=headers,
            stream=True,
            verify=False
        )
        f.write(res.content)

        logger.info(f"Received response: {res.status_code} {res.reason}")
        logger.debug(f"Response headers: {res.headers}")
        # logger.debug(f"Response content: {res.text}")

def _download_file_by_wget(url: str, path_to_save: Path | str):
    wget.download(url, Path(path_to_save))

@retry(
    retry=(
        retry_if_exception_type(httpx.HTTPError) |
        retry_if_exception_type(urllib3.exceptions.HTTPError)
    ),
    stop=stop_after_attempt(5),
    wait=wait_fixed(15),
)
def _download_file_by_httpx(url: str, path_to_save: Path | str):

    with httpx.Client().stream("GET", url) as response:
        response.raise_for_status()

        tmp_path = f"{path_to_save}.{uuid.uuid4()}.tmp"

        with open(tmp_path, "wb") as out_file:
            for chunk in response.iter_raw():
                out_file.write(chunk)

    os.rename(tmp_path, path_to_save)
    return path_to_save


def _download_file(url: str, path_to_save: Path | str, headers: dict[str, str] = None, library: Literal["requests", "wget", "httpx"] = "httpx"):
    if library == "requests":
        _download_file_by_requests(url, path_to_save, headers)
    elif library == "wget":
        _download_file_by_wget(url, path_to_save)
    elif library == "httpx":
        _download_file_by_httpx(url, path_to_save)


def download_file(url: str, path_to_save: Path | str, headers: dict[str, str] = None):
    try:
        _download_file(url, path_to_save, headers, "wget")
    except requests.exceptions.SSLError as e:
        # Log the SSL error with traceback
        logger.error(f"SSL error occurred: {e}")
        logger.exception(e)
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        logger.exception(e)
        raise

def download_image(url: str, _path_to_download: str | Path):
    download_file(url, Path(_path_to_download))

def download_archive(url: str, _path_to_download: str | Path):
    download_file(
        url,
        Path(_path_to_download),
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
    )