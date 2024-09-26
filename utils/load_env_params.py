import os


def load_env_params(params: dict[str, object]):
    for param in params:
        os.environ[param.upper()] = str(params[param])
