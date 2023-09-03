# logging_utils.py
# This module provides functions to set up logging and log information and errors.

import logging
import os

def setup_logging(log_folder='../logging'):
    os.makedirs(log_folder, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_folder, 'errors.log'),
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)