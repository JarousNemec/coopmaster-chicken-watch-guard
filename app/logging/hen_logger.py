import logging
import os.path
import sys
from logging.handlers import RotatingFileHandler

from app import configuration
from app.logging.handler import ColorizedStreamHandler

DEFAULT_FMT = logging.Formatter(
    '%(asctime)s.%(msecs)03d [%(levelname)8s] %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S')


def init_logger():
    config_dir = configuration.get_log_directory()

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    log_file_path = os.path.join(config_dir, configuration.get_log_filename())
    handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 20,
                                  backupCount=10, mode='a')
    handler.setFormatter(DEFAULT_FMT)

    logging.root.setLevel(logging.INFO)
    screen_handler = ColorizedStreamHandler(sys.stdout)
    screen_handler.setFormatter(DEFAULT_FMT)
    logger_i = logging.getLogger()
    logger_i.setLevel(logging.INFO)
    logger_i.addHandler(handler)
    logger_i.addHandler(screen_handler)

    logger = logging.getLogger()
    logger.info( f"Log  file path {log_file_path}." )
    with open("app/resources/banner.txt") as f:
        for line in f.readlines():
            logger.info(line.strip())

    return logger_i

