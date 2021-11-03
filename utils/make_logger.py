"""Return logger instance"""
import logging
from logging import Logger


def create_logger(logger_name, file_name) -> Logger:
    print(f"create logger called to create logger with name {logger_name}")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

    file_handler = logging.FileHandler(file_name)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
