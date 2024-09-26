from pathlib import Path
from utils.split_to_files import _split_file_by_items_count


def split_file_by_count(path_to_parsed_items_file: Path, size_gb: int):
    return _split_file_by_items_count(path_to_parsed_items_file, max_size_gb=size_gb)