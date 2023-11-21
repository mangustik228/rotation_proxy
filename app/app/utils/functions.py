import os


def get_env_prefix(variable: str):
    if os.getenv("MODE") == "DEV":
        return f"DEV_{variable}_"
    elif os.getenv("MODE") == "TEST":
        return f"TEST_{variable}_"
    elif os.getenv("MODE") == "PROD":
        return f"{variable}_"
    else:
        raise ValueError("MODE must be DEV / TEST / PROD")
