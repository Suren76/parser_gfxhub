import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict


class ArchiveSizeItem:
    raw_size: str

    def __init__(self, size):
        self.raw_size = size

    @property
    def size_mb(self):
        _type_of_file = " Mb" if "Mb" in self.raw_size \
            else " Kb" if "Kb" in self.raw_size \
            else " byte" if "byte" in self.raw_size \
            else 0

        _splitted_raw_size = [
            self.raw_size.strip(_type_of_file).replace(",", ".").replace(" ", ""),
            _type_of_file
        ]
        _size_mb = float(_splitted_raw_size[0]) if _splitted_raw_size[1].strip() == "Mb" \
            else float(_splitted_raw_size[0])/1024 if _splitted_raw_size[1].strip() == "Kb" \
            else float(_splitted_raw_size[0])/1024/1024 if _splitted_raw_size[1].strip() == "byte" \
            else 0
        return _size_mb

class ArchiveParsedItem(BaseModel):

    title: str
    url: str
    category: str
    download_links: dict[str, str]
    images: list[str]
    size: str

    @property
    def size_mb(self):
        return ArchiveSizeItem(self.size).size_mb

    _raw = {
        "title": "Nesting Side Tables",
        "url": "https://gfx-hub.co/3d-models/3dsky/92758-nesting-side-tables.html",
        "category": "3DSky",
        "download_links": {"hitf.cc": "https://hitf.cc/uA5tR9d"},
        "images": ["https://gfx-hub.co/uploads/posts/2024-06/nesting_side_tables_0.webp"],
        "size": "11,77 Mb"
    }

    def get_hitfile_download_link(self):
        return self.download_links.get("hitf.cc")

    def get_image_download_link(self):
        return self.images[0]

    @staticmethod
    def get_from_json(raw_json: dict[str, object]) -> list['ArchiveParsedItem']:
        return [ArchiveParsedItem.model_validate(item) for item in raw_json]


class ArchiveParsedItemsList:
    items: list[ArchiveParsedItem]

    def __init__(self, items_list: list[ArchiveParsedItem]):
        self.items = items_list

    def get_lists_of_items_by_size(self, size_gb: int) -> list[list[ArchiveParsedItem]]:
        _size_mb = size_gb*1024

        list_of_items_indexes_splitted_by_size = [0, len(self.items)]

        _size_mb_temp = 0
        for parsed_archive_item in self.items:
            _size_mb_temp += parsed_archive_item.size_mb

            if _size_mb_temp>=_size_mb:
                _size_mb_temp = 0
                list_of_items_indexes_splitted_by_size.append(
                    self.items.index(parsed_archive_item)
                )
        list_of_items_indexes_splitted_by_size.sort()

        return [
            self.items[
                list_of_items_indexes_splitted_by_size[index]: list_of_items_indexes_splitted_by_size[index+1]
            ]
            for index in range(len(list_of_items_indexes_splitted_by_size)-1)
        ]

    def get_lists_of_items_by_count(self, items_count: int, max_size_gb: int) -> list[list[ArchiveParsedItem]]:
        _size_mb = (max_size_gb-1)*1024

        list_of_items_indexes_splitted_by_count = [0, len(self.items)]

        _size_mb_temp = 0
        _count_temp = 0

        parsed_archive_items_sorted = sorted(self.items, key=lambda item: item.size_mb, reverse=True)

        for parsed_archive_item in parsed_archive_items_sorted:
            _size_mb_temp += parsed_archive_item.size_mb
            _count_temp += 1

            if _size_mb_temp>_size_mb or _count_temp >= items_count:
                _size_mb_temp = 0
                _count_temp = 0
                list_of_items_indexes_splitted_by_count.append(parsed_archive_items_sorted.index(parsed_archive_item))

        list_of_items_indexes_splitted_by_count.sort()

        return [
            parsed_archive_items_sorted[
                list_of_items_indexes_splitted_by_count[index]: list_of_items_indexes_splitted_by_count[index+1]
            ]
            for index in range(len(list_of_items_indexes_splitted_by_count)-1)
        ]

    def _size_of_parsed_archive_items_mb(self):
        return sum([item.size_mb for item in self.items])

    def size_mb(self):
        return "{} Mb".format(self._size_of_parsed_archive_items_mb())

    def size_gb(self):
        return "{} Gb".format(self._size_of_parsed_archive_items_mb()/1024)

    def get_items_in_raw_format(self) -> list[dict[str, object]]:
        return [item.model_dump() for item in self.items]

    @staticmethod
    def get_from_file(path_to_file: Path) -> 'ArchiveParsedItemsList':
        return ArchiveParsedItemsList(ArchiveParsedItem.get_from_json(json.loads(open(path_to_file).read())))