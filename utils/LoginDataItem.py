import json
from pathlib import Path


class LoginDataItem:
    login: str
    password: str

    def __init__(self, login, password):
        self.login = login
        self.password = password

    @staticmethod
    def from_raw(raw_format_data: str = None) -> 'LoginDataItem':
        raw_account_data = json.loads(raw_format_data)
        return LoginDataItem.from_dict(raw_account_data)

    def to_dict(self) -> dict:
        return {
            "login": self.login,
            "password": self.password,
        }

    @staticmethod
    def from_dict(account: dict) -> 'LoginDataItem':
        return LoginDataItem(
            login=account.get("login"),
            password=account.get("password"),
        )

    def to_raw(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def get_accounts_list_from_raw_accounts_list(accounts_data_list: list[str]) -> list['LoginDataItem']:
        return [LoginDataItem.from_raw(data) for data in accounts_data_list]

    @staticmethod
    def get_accounts_list_from_dict_accounts_list(accounts_data_list: list[dict]) -> list['LoginDataItem']:
        return [LoginDataItem.from_dict(data) for data in accounts_data_list]

    @staticmethod
    def get_accounts_list_on_json_format(accounts_list: list['LoginDataItem']) -> list[dict]:
        return [account_data.to_dict() for account_data in accounts_list]

    @staticmethod
    def get_accounts_list_on_raw_format(accounts_list: list['LoginDataItem']) -> str:
        return "\n".join([account_data.to_raw() for account_data in accounts_list])

    def __repr__(self):
        return str(self.to_dict())

    def __eq__(self, other: 'LoginDataItem'):
        if isinstance(other, LoginDataItem):
            return self.to_dict() == other.to_dict()
        return NotImplemented
