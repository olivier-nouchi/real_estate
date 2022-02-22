import logging
import requests
import atexit

logger = logging.getLogger(f"scraper.{__name__}")
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds').setLevel(logging.INFO)

import config
import utils
from properties import properties_info, num_properties_with_data, num_properties, Property

# add property id: example: https://phoenix.onmap.co.il/v1/properties/BJOWzFv5K


class Scraper:
    onmap_endpoint = """https://phoenix.onmap.co.il/v1/properties/mixed_search"""
    property_info_endpoint = 'https://phoenix.onmap.co.il/v1/properties/'
    params = {'option': '',
              # 'section': 'residence',
              # '$sort': '-is_top_promoted -search_date',
              '$limit': '300',
              '$skip': '0'}

    num_properties_with_data = num_properties_with_data
    properties_info = properties_info

    session = requests.Session()

    @classmethod
    def scrape_properties_ids(cls, buy_or_rent_option: str) -> list:
        """
        Scrapes the properties ids from the website and saves them in the properties info json
        :param buy_or_rent_option: can take either the value 'rent' or 'buy' or 'both' to combine both options
        :return:
        """

        if buy_or_rent_option == 'both':
            all_properties_ids = []
            for option in ['buy', 'rent']:
                all_properties_ids.extend(cls.scrape_properties_ids(buy_or_rent_option=option))
            return all_properties_ids

        scraped_properties_ids_list = []
        newly_scraped_properties = True

        cls.params['$skip'] = '0'
        cls.params['option'] = buy_or_rent_option

        with cls.session as session:
            while newly_scraped_properties:
                response = session.get(url=cls.onmap_endpoint, params=cls.params)
                data = response.json()['data']

                newly_scraped_properties = [property.get('id') for property in data]
                scraped_properties_ids_list.extend(newly_scraped_properties)
                # To scrape the properties that follow
                cls.params['$skip'] = str(int(cls.params['$skip']) + 300)

        cls.register_properties_ids(scraped_properties_ids_list)
        logger.info(f'Finished scraping properties ids with option {buy_or_rent_option}')

        return scraped_properties_ids_list

    @staticmethod
    def get_properties_ids_without_data(properties_info: dict) -> list:
        """
        Retrieves the properties ids without the data info already in the DB
        :param properties_info:
        :return:
        """
        return [property for property in properties_info if not properties_info[property].get('data')]

    @staticmethod
    def get_properties_ids_with_data(properties_info: dict) -> list:
        """
        Retrieves the properties ids without the data info already in the DB
        :param properties_info:
        :return:
        """
        return [property for property in properties_info if properties_info[property].get('data')]

    @staticmethod
    def register_properties_ids(properties_ids_list: list) -> None:
        """

        :param properties_ids_list:
        :return:
        """
        # We would like to save the properties ids in a file for later retrieval
        existing_properties_ids = utils.load_properties_ids()

        # Only keep the ones which are not already in the json
        properties_ids_to_save = list(set(properties_ids_list) - set(existing_properties_ids))

        for property_id in properties_ids_to_save:
            properties_info[property_id] = dict()

    @classmethod
    def get_list_properties_ids(cls):
        """

        :return:
        """
        scraped_properties_ids_list = []

        existing_properties_ids = utils.load_properties_ids()

        if not existing_properties_ids:
            scraped_properties_ids_list = cls.scrape_properties_ids(buy_or_rent_option='both')

        all_properties_ids = set(existing_properties_ids).union(set(scraped_properties_ids_list))

        return list(all_properties_ids)

    @classmethod
    def scrape_and_register_properties_info(cls, list_properties_ids: list,
                                            buy_or_rent_option: str) -> None:
        """

        :param buy_or_rent_option:
        :param list_properties_ids:
        :return:
        """

        with cls.session as session:
            for property_id in list_properties_ids:
                try:
                    property_info_url = cls.property_info_endpoint + '/' + property_id
                    response = session.get(url=property_info_url)

                    data = response.json()

                    if data:
                        scraping_date = config.TODAY_DATE
                        properties_info[property_id] = {'data': data,
                                                        'scraping_date': scraping_date,}
                                                        # 'buy_or_rent_option': buy_or_rent_option}
                        cls.num_properties_with_data += 1
                except requests.exceptions.RequestException as re:
                    logger.info(re)

                # Save properties info regularly
                if cls.num_properties_with_data % 50 == 0:
                    logger.info(f'Saving scraped properties info...')
                    logger.info(f"{cls.num_properties_with_data}")
                    logger.info(f'Progress: {round(100*cls.num_properties_with_data/num_properties)}%')
                    Property.save_properties_info(properties_info)


def scrape_properties_from_onmap(buy_or_rent_option: str = 'both') -> None:
    """
    :param:
    :return:
    """
    # TODO: scrape the properties only if data older than 1 week OR force_scraping flag is True
    scraped_properties_ids = Scraper.scrape_properties_ids(buy_or_rent_option=buy_or_rent_option)
    without_data_properties_ids = Scraper.get_properties_ids_without_data(properties_info=properties_info)
    properties_ids_with_data = Scraper.get_properties_ids_with_data(properties_info=properties_info)
    properties_ids_to_scrape = list(set(scraped_properties_ids).union(set(without_data_properties_ids)) - set(properties_ids_with_data))
    logger.info(f"number properties ids to scrape {len(properties_ids_to_scrape)}")
    Scraper.scrape_and_register_properties_info(list_properties_ids=properties_ids_to_scrape,
                                                buy_or_rent_option=buy_or_rent_option)


def exit_handler():
    Property().save_properties_info(properties_info=properties_info)


def main():
    scrape_properties_from_onmap(buy_or_rent_option='both')
    atexit.register(exit_handler)


if __name__ == '__main__':
    main()