from bookingSystem.logger import setup_logger
from datetime import datetime

import pytz

logger = setup_logger()

tz = pytz.timezone("Asia/Taipei")


def my_task():
    # logger.info("1111")
    print("my_task ****", datetime.now(tz))
