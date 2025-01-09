import logging
import requests
from requests.adapters import HTTPAdapter, Retry

from app.core.config import BASE_URL

logger = logging.getLogger("AWSClient")


class AWSClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_url: str = BASE_URL):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.base_url = base_url
        self._allowed_ips = self.fetch_data()
        self._initialized = True

    def fetch_data(self):
        """Fetch IP addresses from Amazon"""
        session = requests.session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        session.mount('https://', HTTPAdapter(max_retries=retries))
        response = session.get(self.base_url)

        if response.status_code == 200:
            logger.info("Successfully fetched data from %s", self.base_url)
            data = response.json()
            regions = ["eu-west-1", "eu-west-2", "eu-west-3"]
            self._allowed_ips = {
                prefix["ip_prefix"]
                for prefix in data["prefixes"]
                if prefix["region"] in regions
            }
            return self._allowed_ips

        logger.error("Failed to fetch IP from AWS. Status code: %s", response.status_code)
        return None
