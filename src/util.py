from os import getenv

def get_env(key: str):
    v = getenv(key, None)
    if v is None:
        raise ValueError(f"No {key} found in environment")
    return v