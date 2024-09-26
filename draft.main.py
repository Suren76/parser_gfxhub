from pathlib import Path
from utils.hitfile_utils import get_download_url_of_archive
from utils.hitfile_utils import get_archive_metadata
from utils.cookies_utils import get_headers_of_account_with_auth
from utils.download_files_utils import download_file

headers = get_headers_of_account_with_auth(Path("/home/suren/Projects/upwork/maroz/parser_gfxHub/resources/login_account_data.json"))
url = "https://hitfile.net/2xkxqH6"

try:
    url_to_download_archive = get_download_url_of_archive(url, headers)
    archive_download_metadata = get_archive_metadata(url, headers)
except Exception as e:print(e)

download_file(url_to_download_archive, "./resources/archive_download_test/test_archive_extension.rar")