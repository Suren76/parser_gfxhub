from pathlib import Path

from utils.ArchiveParseModels import ArchiveParsedItemsList


def get_size_of_file(path_to_parsed_items_file: Path):
    return ArchiveParsedItemsList.get_from_file(path_to_parsed_items_file).size_mb()