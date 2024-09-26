#!/home/suren/.cache/pypoetry/virtualenvs/slack-bot-e3O-PR5L-py3.11/bin/python3.11

import argparse

from pathlib import Path

from extra_utils.get_delta_of_two_files import delta_of_two_files
from extra_utils.get_downloaded_archives_list import get_downloaded_archives_list
from extra_utils.get_size_of_file import get_size_of_file
from extra_utils.split_file_by_items_count import split_file_by_count
from extra_utils.split_file_by_size import split_file_by_size
from main import main_actions

parser = argparse.ArgumentParser()

parser.add_argument("action", help="set the mode main script to work", choices=['scraper', 'downloader', "extra"])

parser.add_argument("-parsed-file", "--path-to-archives-parsed-items-file", help="get path of file where parsed archive items list writes data.", type=str)
parser.add_argument("-split-size", "--split-size-for-parsed-items-file", help="size by which parsed archive items file should be splitted", type=int)
parser.add_argument("-O", "--output-directory", help="sets the folder where files will be saved", type=str)
parser.add_argument("-data", "--login-data", help="get path to login data file and set folder as a env variable store path", type=str)
parser.add_argument("--DEBUG", action='store_true')


subparser = parser.add_subparsers()

# action_parser = subparser.add_parser("action", help="'scraper' and 'downloader'")


# action_parser.add_argument("-d", "--directory", help="get path to directory and set as files folder")
# action_parser.add_argument("-O", "--output-directory", help="sets the folder where files will be saved")
# action_parser.add_argument("-data", "--login-data", help="get path to login data file and set folder as a env variable store path")


extra_tools_parser = subparser.add_parser(
    "extra_tools",
    help=
    "command to run extra tools which is not included in main app functionality."
    "you can pass 'delta_of_files', 'size_of_file', 'split_by_size' values to run.",
    formatter_class=argparse.RawTextHelpFormatter
)

extra_tools_parser.add_argument(
    "extra_tool_to_run",
    type=str,
    choices=['delta_of_files', 'size_of_file', 'split_by_size', 'get_downloaded_archives_list'],
    help=
    'delta_of_files -old-file="<PATH_TO_OLD_FILE>" -new-file="<PATH_TO_NEW_FILE>" \n' 
    'size_of_file -parsed-items-file="<PATH_TO_PARSED_ARCHIVE_ITEMS_FILE>" \n'
    'split_by_size -parsed-items-file="<PATH_TO_PARSED_ARCHIVE_ITEMS_FILE>" -size-gb=<SIZE_IN_GB> \n'
    'get_downloaded_archives_list -downloaded-archives-folder="<PATH_TO_DOWNLOADED_ARCHIVES_FOLDER>" -parsed-items-file="<PATH_TO_PARSED_ARCHIVE_ITEMS_FILE>" \n'
)

extra_tools_parser.add_argument("-old-file", "--extra-tools-file-old", help="get path to old parsed archive items file")
extra_tools_parser.add_argument("-new-file", "--extra-tools-file-new", help="get path to new parsed archive items file")

extra_tools_parser.add_argument("-parsed-items-file", "--extra-tools-path-to-parsed-items-file", help="get path to parsed archive items file")
extra_tools_parser.add_argument("-downloaded-archives-folder", "--extra-tools-path-to-downloaded-archives-folder", help="get path to downloaded archives folder")
extra_tools_parser.add_argument("-size-gb", "--extra-tools-size-gb", help="size of parsed archive items file to split")


args = parser.parse_args()

if args.DEBUG: print(args)
if "extra" in args.action:
    if "extra_tool_to_run" in args:
        tool_name = args.extra_tool_to_run

        extra_tools_file_old: Path = Path(args.extra_tools_file_old) if args.extra_tools_file_old else None
        extra_tools_file_new: Path = Path(args.extra_tools_file_new) if args.extra_tools_file_new else None
        extra_tools_path_to_parsed_items_file: Path = Path(args.extra_tools_path_to_parsed_items_file) if args.extra_tools_path_to_parsed_items_file else None
        extra_tools_path_to_downloaded_archives_folder: Path = Path(args.extra_tools_path_to_downloaded_archives_folder) if args.extra_tools_path_to_downloaded_archives_folder else None
        extra_tools_size_gb: int = int(args.extra_tools_size_gb) if args.extra_tools_size_gb else None

        if tool_name == "delta_of_files":
            delta_of_two_files(path_to_old_file=extra_tools_file_old, path_to_new_file=extra_tools_file_new)
        if tool_name == "size_of_file":
            print(get_size_of_file(path_to_parsed_items_file=extra_tools_path_to_parsed_items_file))
        if tool_name == "get_downloaded_archives_list":
            get_downloaded_archives_list(extra_tools_path_to_downloaded_archives_folder, extra_tools_path_to_parsed_items_file)
        if tool_name == "split_by_size":
            split_file_by_count(path_to_parsed_items_file=extra_tools_path_to_parsed_items_file, size_gb=extra_tools_size_gb)

        exit(0)

action = args.action
path_to_archives_parsed_items_file: Path = Path(args.path_to_archives_parsed_items_file) if args.path_to_archives_parsed_items_file else None
split_size_for_parsed_items_file = int(args.split_size_for_parsed_items_file) if args.split_size_for_parsed_items_file else None
path_to_output_directory: Path = Path(args.output_directory) if args.output_directory else None
login_data: Path = Path(args.login_data) if args.login_data else None


main_actions(
    _action=action,
    _path_to_archive_parsed_items_file=path_to_archives_parsed_items_file,
    _parser_items_file_split_size=split_size_for_parsed_items_file,
    _path_to_save_directory=path_to_output_directory,
    _debug=args.DEBUG,
    _path_to_login_datas_file=login_data,
)