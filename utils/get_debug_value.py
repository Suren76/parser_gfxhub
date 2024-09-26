import os


def get_debug_value() -> bool:
    return bool(os.environ.get("DEBUG"))