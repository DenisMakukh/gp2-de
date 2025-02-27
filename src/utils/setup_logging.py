"""
Module Description:
Module destined for logging setup.

Author: Denis Makukh
Date: 27.02.2025
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    log_directory = '.log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)
        os.chmod(log_directory, 0o755)

    log_file = os.path.join(log_directory, 'app.log')

    file_handler = TimedRotatingFileHandler(filename=log_file,
                                            when='W0',
                                            backupCount=2,
                                            encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] In module: %(module)s; In function: %('
                                       'funcName)s(); Message: %(message)s')
    file_handler.setFormatter(file_formatter)

    logger_conf = logging.getLogger()
    logger_conf.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] In module: %(module)s; In function: %('
                                          'funcName)s(); Message: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger_conf.addHandler(console_handler)
    logger_conf.setLevel(logging.INFO)
