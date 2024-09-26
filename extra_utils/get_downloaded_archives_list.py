import json
from pathlib import Path

from utils.ArchiveParseModels import ArchiveParsedItemsList
from utils.download_by_item import check_is_archive_downloaded, DownloadItem
from utils.hitfile_utils import get_name_of_archive


def get_downloaded_archives_list(path_to_archives_folder: Path, path_to_parsed_archive_items_file: Path):
    parsed_archives_list: ArchiveParsedItemsList = ArchiveParsedItemsList.get_from_file(path_to_parsed_archive_items_file)
    parsed_archives_list_progress = {
        item.title: {
            "download_done": False,
            "item": item.model_dump()
        }
        for item in parsed_archives_list.items
    }

    for parsed_archive_item in parsed_archives_list.items:
        archive_download_item = DownloadItem("None", get_name_of_archive(parsed_archive_item.get_hitfile_download_link(), {}))
        if check_is_archive_downloaded(parsed_archive_item, archive_download_item, path_to_archives_folder):
            parsed_archives_list_progress[parsed_archive_item.title]["download_done"] = True

    with open(path_to_parsed_archive_items_file.with_stem("STATISTIC_" + path_to_parsed_archive_items_file.stem),"w+") as file_of_result:
        file_of_result.write(json.dumps(parsed_archives_list_progress))

