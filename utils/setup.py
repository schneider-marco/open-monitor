import os
import sys
from utils import logger

def setup():
    files_to_check = [
        "/app/config/config.yaml",
        "/app/ansible/inventory/inventory.ini"
    ]
    directories_to_check = [
        "/app/ansible/sshkeys/",
        "/app/ansible/playbooks/"
    ]

    # Check if required files exist
    for file_path in files_to_check:
        if not os.path.isfile(file_path):
            logger.error(f"Error: The file '{file_path}' does not exist.")
            sys.exit(1)

    # Check if required directories exist and are not empty
    for dir_path in directories_to_check:
        if not os.path.isdir(dir_path):
            logger.error(f"Error: The directory '{dir_path}' does not exist.")
            sys.exit(1)

    logger.debug("Setup completed successfully. All required files and directories are present.")
