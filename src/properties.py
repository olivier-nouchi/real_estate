import json

import logging
import config
from utils import load_properties_info

logger = logging.getLogger(f"scraper.{__name__}")


class Property:
    id: str

    @staticmethod
    def load_properties() -> dict:
        """

        :return:
        """
        return load_properties_info()

    @staticmethod
    def count_unique_properties(properties: dict) -> int:
        """

        :return:
        """
        return len(set(properties))

    @staticmethod
    def count_properties(properties: dict) -> int:
        """

        :return:
        """
        return len(properties)

    @staticmethod
    def count_properties_with_info(properties: dict) -> int:
        """
        Counts the number of properties with info
        :param properties:
        :return:
        """
        return sum(1 for property in properties if properties[property].get('data'))

    @staticmethod
    def save_properties_info(properties_info: dict) -> None:
        """

        :param properties_info:
        :return:
        """
        if properties_info:
            with open(config.properties_info_filepath, 'w') as file:
                json.dump(properties_info, file)
        else:
            logger.info(f'properties info object is either empty or does not exist')


properties_info = load_properties_info()
num_unique_properties = Property().count_unique_properties(properties=properties_info)
num_properties = Property().count_properties(properties=properties_info)
num_properties_with_data = Property().count_properties_with_info(properties=properties_info)
logger.info(f"number unique properties {num_unique_properties}")
logger.info(f"number properties {num_properties}")
logger.info(f"number properties with data {num_properties_with_data}")
