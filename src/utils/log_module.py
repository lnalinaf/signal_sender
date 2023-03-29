import os

from loguru import logger

log_path = os.path.expanduser("myapp.log")


def setup_logger():
    logger.add(
        log_path,
        rotation="100 MB",
        level="DEBUG",
        format="{time:x}"
        + " | {module}:{name}:{function}:{line} - {message} ",
    )

    return logger
