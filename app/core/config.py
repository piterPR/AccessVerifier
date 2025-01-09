import os
import logging

BASE_URL = os.getenv("AWS_BASE_URL", "https://ip-ranges.amazonaws.com/ip-ranges.json")
SCHEDULER_INTERVAL_HOURS = os.getenv("SCHEDULER_INTERVAL_HOURS", "24")
DATA_PATH  = os.getenv("DATA_PATH", "app/data/data.json")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


## logging config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)
