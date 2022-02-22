import json
import os
import time
from datetime import datetime
from collections import defaultdict

import config
import logging

NUM_SECONDS_IN_DAYS = 60 * 60 * 24

logger = logging.getLogger(f"scraper.{__name__}")


def load_properties_info() -> dict:
    """
    Loads the properties info from the json
    :return:
    """

    properties_info = defaultdict(dict)
    try:
        with open(config.properties_info_filepath, 'r') as file:
            properties_info = json.load(file)

    except FileNotFoundError as fnfe:
        logger.info(f'The properties info file was not found {fnfe}.')

    return properties_info


def load_properties_ids() -> list:
    """

    :return:
    """
    properties_ids = []
    try:
        with open(config.properties_info_filepath, 'r') as file:
            properties_info = json.load(file)
            properties_ids = list(properties_info.keys())

    except FileNotFoundError as fnfe:
        logger.info(f'The properties ids file was not found {fnfe}.')

    return properties_ids


def time_from_last_modif_file(filepath: str) -> time:
    """
    Calculates the amount of time elapsed between now and the last modif of a file
    :return:
    """
    try:
        last_modif_file = os.path.getmtime(filepath)
    except FileNotFoundError:
        last_modif_file = 0
    now_time = int(time.time())

    return (now_time - last_modif_file) / NUM_SECONDS_IN_DAYS


def get_unique_ids_from_several_lists(*args) -> list:
    """

    :param args:
    :return:
    """
    res = []
    for my_list in args:
        res += my_list
    return res


def format_datetime(datetime_with_timezone_str: str):
    datetime_with_timezone = datetime(datetime_with_timezone_str)
    # dt = datetime_with_timezone_.replace(tzinfo=None)
    formatted_dt = datetime.strptime(datetime_with_timezone, "%Y-%m-%d")

    return formatted_dt


# properties_info = load_properties_info()
# num_properties = count_properties(properties=properties_info)
# num_properties_with_data = count_properties_with_info(properties=properties_info)
# logger.info(f"number properties with data {num_properties_with_data}")
