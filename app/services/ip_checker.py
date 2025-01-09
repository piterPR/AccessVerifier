import json
import logging
import ipaddress
from fastapi import HTTPException

logger = logging.getLogger("IPChecker")


class IPChecker:
    """
    DataReader class for reading IP from saved file
    """
    def __init__(self, body: str):
        self.body = body

    def check_ip(self):
        """
        Check if ip address is within fetched data from AWS IP address ranges
        """
        client_ip = self._extract_client_ip()
        allowed_ips = self._read_allowed_ips()
        return self._is_ip_allowed(client_ip, allowed_ips)

    def _extract_client_ip(self):
        """
        Extract the client IP address from the HTTP headers.
        """
        header_lines = self.body.decode("utf-8").splitlines()
        for line in header_lines:
            if line.lower().startswith("x-forwarded-for:"):
                client_ip = line.split(":")[1].strip()
                logger.debug("Extracted client IP: %s", client_ip)
                return client_ip

        logger.warning("Client IP not found in plain/text POST.")
        raise HTTPException(status_code=400, detail="Client IP not found in headers")

    def _is_ip_allowed(self, client_ip, allowed_ips):
        """
        Check if the client IP is within the allowed IP ranges.
        """
        try:
            client_ip_obj = ipaddress.ip_address(client_ip)
        except ValueError as error:
            logger.error("Invalid IP address: %s", client_ip)
            raise HTTPException(status_code=400, detail="Invalid IP address") from error
        for cidr in allowed_ips:
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                if client_ip_obj in network:
                    return True
            except ValueError as error:
                logger.error("Invalid CIDR in data: %s", cidr)

        logger.warning("Client IP %s is not allowed.", client_ip)
        return False

    def _read_allowed_ips(self):
        """
        Read the list of allowed IPs from a JSON file.
        """
        try:
            with open("app/data/data.json", "r", encoding="utf-8") as file:
                allowed_ips = json.load(file)
            return allowed_ips
        except (FileNotFoundError, json.JSONDecodeError) as error:
            logger.error("Error reading allowed IPs from file: %s", error)
            raise HTTPException(status_code=500, detail="Server configuration error") from error
