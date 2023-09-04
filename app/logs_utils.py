# logging_utils.py
# This module provides functions to set up logging and log information and errors.

import logging
import os

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
user_folder = os.path.expanduser("~")
current_directory = os.getcwd()
log_file = "errors.log"
log_path = os.path.join(current_directory, app_dir)

def setup_logging(log_folder=log_path):
    os.makedirs(log_folder, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_folder, log_file),  # Use the log_folder here, not the log_path
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_info(message):
    logging.info(message)
    print(f"Log saved location: {os.path.join(log_path, log_file)}")

def log_error(message):
    logging.error(message)
    print(f"Log saved location: {os.path.join(log_path, log_file)}")