import logging
from logging import Logger

logging.basicConfig(level=logging.INFO)

def get_logger(prefix: str) -> Logger:
    logger = logging.getLogger(f'[{prefix}]')
    logger.setLevel(logging.INFO)
    return logger
