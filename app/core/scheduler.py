import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.data_fetcher import DataFetcher
from app.api.clients.aws_client import AWSClient

logger = logging.getLogger("DataScheduler")

class DataScheduler:
    def __init__(self, base_url: str, data_path: str):
        self.scheduler = BackgroundScheduler()
        self.client = AWSClient(base_url=base_url)
        self.fetcher = DataFetcher(api_client=self.client, data_path=data_path)

    def start(self, interval=24):
        """Scheduler for setting jobs"""
        self.fetcher.fetch_and_save()
        self.scheduler.configure(timezone="Europe/Warsaw")
        fetch_data = self.scheduler.add_job(self.fetcher.fetch_and_save, 'interval', hours=int(interval))
        self.scheduler.start()
        logger.info("Next scheduled task at: %s", fetch_data.next_run_time)
