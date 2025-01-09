import logging
import ipaddress
import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger("AWSClient")


class AWSClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._allowed_ips = set()

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
            regions = ["eu-west-1", "eu-west-2"]
            self._allowed_ips = {
                prefix["ip_prefix"]
                for prefix in data["prefixes"]
                if prefix["region"] in regions
            }
            return self._allowed_ips

        logger.error("Failed to fetch IP from AWS. Status code: %s", response.status_code)
        return None

    def get_allowed_ips(self):
        """Get the list of allowed IPs"""
        if not self._allowed_ips:
            logger.warning("Allowed IPs are not loaded. Please fetch data first.")
        return self._allowed_ips

    def is_ip_allowed(self, ip: str):
        """Check if a given IP is in the allowed list"""
        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            logger.warning("Invalid IP address provided: %s", ip)
            return False

        for cidr in self._allowed_ips:
            if ip_obj in ipaddress.ip_network(cidr):
                return True

        logger.info("IP %s is not allowed.", ip)
        return False
