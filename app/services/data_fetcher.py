import json
import logging
from app.api.clients.aws_client import AWSClient

logger = logging.getLogger("DataFetcher")


class DataFetcher:
    """
    DataFetcher class for save data form aws into data_path
    """
    def __init__(self, api_client: AWSClient, data_path: str = "app/data/data.json"):
        self.api_client = api_client
        self.data_path = data_path

    def fetch_and_save(self):
        """
        Save data into file 
        """
        data = self.api_client.fetch_data()
        if data:
            try:
                with open(self.data_path, "w", encoding="utf-8") as file:
                    json.dump(list(data), file)
                logger.info("Data successfully fetched and saved to %s.",self.data_path)
            except PermissionError:
                logger.error("Permission denied: Unable to write to %s.", self.data_path)
            except IOError as error:
                logger.error("IO error while saving data to %s: {e}",error)
        else:
            logger.error("No data received from API. Fetching operation failed.")
