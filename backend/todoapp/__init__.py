import logging


def get_logger(name: str = "") -> logging.Logger:
    if name:
        name = f".{name}"

    return logging.getLogger(f"uvicorn.error{name}")
