import logging
import ipaddress
from fastapi import HTTPException
from app.api.clients.aws_client import AWSClient


logger = logging.getLogger("IPChecker")


class IPChecker:

    @staticmethod
    def check_ip(body: str, self):
        """
        Check if ip address is within fetched data from AWS IP address ranges
        """
        client_ip = self._extract_client_ip(body=body)
        return self._is_ip_allowed(client_ip)

    @staticmethod
    def _extract_client_ip(body: str):
        """
        Extract the client IP address from the HTTP headers.
        """
        header_lines = body.decode("utf-8").splitlines()
        for line in header_lines:
            if line.lower().startswith("x-forwarded-for:"):
                client_ip = line.split(":")[1].strip()
                logger.debug("Extracted client IP: %s", client_ip)
                return client_ip

        logger.warning("Client IP not found in plain/text POST.")
        raise HTTPException(status_code=400, detail="Client IP not found in headers")

    @staticmethod
    def _is_ip_allowed(client_ip):
        """
        Check if the client IP is within the allowed IP ranges.
        """
        try:
            client_ip_obj = ipaddress.ip_address(client_ip)
        except ValueError as error:
            logger.error("Invalid IP address: %s", client_ip)
            raise HTTPException(status_code=400, detail="Invalid IP address") from error
        for cidr in AWSClient().getAllowedIPs():
            try:
                network = ipaddress.ip_network(cidr, strict=False)
                if client_ip_obj in network:
                    return True
            except ValueError as error:
                logger.error("Invalid CIDR in data: %s", error)

        logger.warning("Client IP %s is not allowed.", client_ip)
        return False
