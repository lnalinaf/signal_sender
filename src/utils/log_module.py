import os
import sys

from loguru import logger

log_path = os.path.expanduser("myapp.log")


def setup_logger():
    # logger.add(
    #     log_path,
    #     rotation="100 MB",
    #     level="INFO",
    #     # level="DEBUG",
    #     format="{time:x}"
    #     + " | {module}:{name}:{function}:{line} - {message} ",
    # )
    logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])

    return logger
