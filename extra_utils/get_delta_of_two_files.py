import json
from pathlib import Path

from tqdm import tqdm

from utils.ArchiveParseModels import ArchiveParsedItemsList, ArchiveParsedItem


def delta_of_two_files(path_to_old_file: Path, path_to_new_file: Path):
    old_parsed_archive_items = ArchiveParsedItemsList.get_from_file(path_to_old_file).items
    new_parsed_archive_items = ArchiveParsedItemsList.get_from_file(path_to_new_file).items

    __old_parsed_archive_items_links = [
        parsed_archive_item.get_hitfile_download_link()
        for parsed_archive_item in old_parsed_archive_items
    ]

    _delta_of_parsed_archive_items_list: list[ArchiveParsedItem] = [
        parsed_archive_item
        for parsed_archive_item in tqdm(new_parsed_archive_items)
        if parsed_archive_item.get_hitfile_download_link() not in __old_parsed_archive_items_links
    ]

    path_to_delta_file: Path = Path(path_to_new_file.with_stem("DELTA_" + path_to_new_file.stem + "__" + path_to_old_file.stem))
    with open(path_to_delta_file, "w+") as delta_file:
        delta_file.write(json.dumps(ArchiveParsedItemsList(_delta_of_parsed_archive_items_list).get_items_in_raw_format()))
