import json
import os.path
from pathlib import Path

from utils.ArchiveParseModels import ArchiveParsedItemsList, ArchiveParsedItem


def _save_to_files_list_of_items(_path_to_save_folder: Path, lists_of_items: list[list[ArchiveParsedItem]], filename: Path):
    for items_list in lists_of_items:
        _filename: Path = filename.with_stem(filename.stem + "_{}__{}Gb".format(
            lists_of_items.index(items_list)+1, ArchiveParsedItemsList(items_list).size_gb()[:5]
        ))
        with open(_path_to_save_folder / _filename, "w+") as file:
            file.write(json.dumps(ArchiveParsedItemsList(items_list).get_items_in_raw_format()))

def _split_file_by_size(_path_to_parsed_archives_file: Path, size_gb: int = 80):
    parsed_archives_list: ArchiveParsedItemsList = ArchiveParsedItemsList.get_from_file(_path_to_parsed_archives_file)
    list_of_splitted_items_list = parsed_archives_list.get_lists_of_items_by_size(size_gb)

    _path_to_save_folder: Path = _path_to_parsed_archives_file.parent / (_path_to_parsed_archives_file.stem + "_{}Gb".format(size_gb))
    _filename_of_splitted_file: Path = Path(_path_to_parsed_archives_file.name).with_stem(_path_to_parsed_archives_file.stem + "_splitted")

    if not os.path.exists(_path_to_save_folder): os.mkdir(_path_to_save_folder)

    _save_to_files_list_of_items(_path_to_save_folder, list_of_splitted_items_list, _filename_of_splitted_file)


def _split_file_by_items_count(_path_to_parsed_archives_file: Path, items_count: int = 250, max_size_gb: int = 80):
    parsed_archives_list: ArchiveParsedItemsList = ArchiveParsedItemsList.get_from_file(_path_to_parsed_archives_file)
    list_of_splitted_items_list = parsed_archives_list.get_lists_of_items_by_count(items_count, max_size_gb)

    _path_to_save_folder: Path = _path_to_parsed_archives_file.parent / (_path_to_parsed_archives_file.stem + "_{}Gb__{}count".format(max_size_gb, items_count))
    _filename_of_splitted_file: Path = Path(_path_to_parsed_archives_file.name).with_stem(_path_to_parsed_archives_file.stem + "_splitted")

    if not os.path.exists(_path_to_save_folder): os.mkdir(_path_to_save_folder)

    _save_to_files_list_of_items(_path_to_save_folder, list_of_splitted_items_list, _filename_of_splitted_file)



