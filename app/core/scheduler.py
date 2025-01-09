import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.core.config import SCHEDULER_INTERVAL_HOURS
from app.api.clients.aws_client import AWSClient

logger = logging.getLogger("DataScheduler")

class DataScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._start(interval=SCHEDULER_INTERVAL_HOURS)

    def _start(self, interval=24):
        """Scheduler for setting jobs"""
        self.scheduler.configure(timezone="Europe/Warsaw")
        fetch_data = self.scheduler.add_job(AWSClient().fetch_data, 'interval', hours=int(interval))
        self.scheduler.start()
        logger.info("Next scheduled task at: %s", fetch_data.next_run_time)
