import os
import logging


def setup_logger():
    app_name = "bookingSystem"
    log_dir = os.path.join(os.getcwd(), "logs", app_name)
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, app_name + ".log")

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
