import json
from pathlib import Path


def filter_data(data: list[dict[str, str]]):
    filtered_data = {}
    for item in data:
        if filtered_data.get(item.get("category")) is None: filtered_data[item.get("category")] = []

        filtered_data[item["category"]].append(
            {
                "title": item["title"],
                "url": item["url"],
                "download_links": item["download_links"],
            }
        )
    return filtered_data


def filter_data_from_file(path_to_file: Path | str):
    path_to_file = Path(path_to_file)

    data = json.loads(open(path_to_file).read())
    filtered_data = filter_data(data)
    open(path_to_file.with_stem(path_to_file.stem + "_filtered"), "w+").write(json.dumps(filtered_data))
