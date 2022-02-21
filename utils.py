import json
import os
import time
import atexit
from collections import defaultdict

import config
import logging

global properties_info
global num_properties_with_data

NUM_SECONDS_IN_DAYS = 60 * 60 * 24

logger = logging.getLogger(f"{__name__}")


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


def save_properties_info() -> None:
    """

    :param properties_info:
    :return:
    """
    if properties_info:
        with open(config.properties_info_filepath, 'w') as file:
            json.dump(properties_info, file)
    else:
        logger.info(f'properties info object is either empty or does not exist')


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


def count_properties_with_info(properties: dict) -> int:
    """
    Counts the number of properties with info
    :param properties:
    :return:
    """
    return sum(1 for property in properties_info if properties_info[property].get('data'))


def get_unique_ids_from_several_lists(*args) -> list:
    """

    :param args:
    :return:
    """
    res = []
    for my_list in args:
        res += my_list
    return res


def count_properties(properties: dict) -> int:
    """
    Counts the number of properties with info
    :param properties:
    :return:
    """
    return len(properties)


def exit_handler():
    save_properties_info()


properties_info = load_properties_info()
# number of properties with data
num_properties = count_properties(properties=properties_info)
num_properties_with_data = count_properties_with_info(properties=properties_info)
atexit.register(exit_handler)
logger.info("number properties with data", num_properties_with_data)
