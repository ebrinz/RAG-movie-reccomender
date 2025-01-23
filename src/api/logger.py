# logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='movie_api', log_file='app.log'):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = os.path.join(log_dir, log_file)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

logger = setup_logger()

def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)