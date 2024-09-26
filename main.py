from datetime import datetime
from pathlib import Path
from typing import Literal

from loguru import logger

from gfxHUB_spider import run_parser
from utils.download_by_item import download_by_file
from utils.load_env_params import load_env_params
from utils.split_to_files import _split_file_by_items_count


def archives_scraper(path_to_parse_archive_items_file: Path, parser_items_file_split_size: int):
    run_parser(path_to_parse_archive_items_file)
    _split_file_by_items_count(path_to_parse_archive_items_file, max_size_gb=parser_items_file_split_size)

def archives_downloader(path_to_parse_archive_items_file: Path, path_to_save_folder: Path):
    download_by_file(path_to_parse_archive_items_file, path_to_save_folder)

@logger.catch
def main_actions(
        _action:Literal['scraper', 'downloader'],
        _path_to_archive_parsed_items_file: Path,
        _path_to_save_directory: Path,
        _debug: bool,
        _path_to_login_datas_file: Path,
        _parser_items_file_split_size: int,
):
    # setup env variables
    load_env_params({
        "PATH_TO_LOGIN_FILE": _path_to_login_datas_file,
        "DEBUG": _debug
    })

    path_to_logs_file = Path(_path_to_save_directory) / f"logs_{datetime.now().strftime('%Y.%m.%d_%H-%M-%S')}.json"

    logger.add(
        path_to_logs_file,
        level="DEBUG",
        format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
        serialize=True
    )


    if _action == 'scraper':
        archives_scraper(_path_to_archive_parsed_items_file, _parser_items_file_split_size)
    if _action == 'downloader':
        archives_downloader(_path_to_archive_parsed_items_file, _path_to_save_directory)
