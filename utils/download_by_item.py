import json
import os.path
from pathlib import Path

from typing import NamedTuple

from loguru import logger
from tqdm import tqdm

from utils.ArchiveParseModels import ArchiveParsedItem, ArchiveParsedItemsList
from utils.cookies_utils import get_headers_of_account_with_auth, get_path_to_login_file
from utils.download_utils import download_image, download_archive
from utils.get_debug_value import get_debug_value
from utils.hitfile_utils import get_archive_metadata, ArchiveDownloadMetadata


class DownloadItem(NamedTuple):
    download_url: str
    filename: str | Path

def _get_archive_metadata(url: str) -> ArchiveDownloadMetadata:
    _path_to_login_file: Path = get_path_to_login_file()
    headers = get_headers_of_account_with_auth(_path_to_login_file)
    return get_archive_metadata(url, headers)

def _get_archive_download_item(archive_download_url: str) -> DownloadItem:
    _archive_download_metadata: ArchiveDownloadMetadata = _get_archive_metadata(archive_download_url)

    _url = _archive_download_metadata.link
    _filename = _archive_download_metadata.name
    return DownloadItem(_url, Path(_filename))

def _get_image_download_item(image_download_url: str) -> DownloadItem:
    _url = image_download_url
    _filename = Path(image_download_url).name
    return DownloadItem(_url, Path(_filename))


def check_is_archive_downloaded(archive_parsed_item: ArchiveParsedItem, archive_download_item: DownloadItem, path_to_download_folder: Path):
    path_to_downloaded_archive = path_to_download_folder / archive_download_item.filename
    if os.path.exists(path_to_downloaded_archive):
        size_of_downloaded_archive = round(os.path.getsize(path_to_downloaded_archive) / (1024*1024), 2)
        if get_debug_value(): logger.debug(f"{path_to_downloaded_archive=}, {size_of_downloaded_archive=}, {archive_parsed_item.size_mb=}")
        return  size_of_downloaded_archive == archive_parsed_item.size_mb
    return False

def download_item(archive_parsed_item: ArchiveParsedItem, path_to_download_folder: Path | str):
    _path_to_download_folder: Path = Path(path_to_download_folder)

    image_download_item: DownloadItem = _get_image_download_item(archive_parsed_item.get_image_download_link())
    archive_download_item: DownloadItem = _get_archive_download_item(archive_parsed_item.get_hitfile_download_link())

    if check_is_archive_downloaded(archive_parsed_item, archive_download_item, path_to_download_folder): return

    if get_debug_value(): logger.debug(f"Downloading -- filename: [{archive_parsed_item.title}] | size: [{archive_parsed_item.size_mb}Mb] ")

    download_image(image_download_item.download_url, _path_to_download_folder / image_download_item.filename.with_stem(archive_download_item.filename.stem))
    download_archive(archive_download_item.download_url, _path_to_download_folder / archive_download_item.filename)

# TODO: rename function
def download_by_file(path_to_parsed_archive_items_file: Path, path_to_save_folder: Path):
    parsed_archives_list: ArchiveParsedItemsList = ArchiveParsedItemsList.get_from_file(path_to_parsed_archive_items_file)
    parsed_archives_list_progress = {
        item.title: {
            "download_done": False,
            "item": item.model_dump()
        }
        for item in parsed_archives_list.items
    }
    try:
        for parsed_archive_item in (_pbar := tqdm(parsed_archives_list.items, desc="download_by_file phase")):
            if not get_debug_value(): _pbar.set_description(f"{'download_by_file phase'} | size: [{parsed_archive_item.size_mb}Mb] filename: [{parsed_archive_item.title}] ")

            download_item(parsed_archive_item, path_to_save_folder)
            parsed_archives_list_progress[parsed_archive_item.title]["download_done"] = True
    finally:
        with open(path_to_parsed_archive_items_file.with_stem("RESULT_" + path_to_parsed_archive_items_file.stem), "w+") as file_of_result:
            file_of_result.write(json.dumps(parsed_archives_list_progress))

