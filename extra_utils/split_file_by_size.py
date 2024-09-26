from pathlib import Path
from utils.split_to_files import _split_file_by_size


def split_file_by_size(path_to_parsed_items_file: Path, size_gb: int):
    return _split_file_by_size(path_to_parsed_items_file, size_gb)