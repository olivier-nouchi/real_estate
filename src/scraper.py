import requests
import json
import logging

import config

logger = logging.getLogger(__name__)


# add property id: example: https://phoenix.onmap.co.il/v1/properties/BJOWzFv5K


# logger: https://realpython.com/python-logging/

class Scraper:
    onmap_endpoint = """https://phoenix.onmap.co.il/v1/properties/mixed_search"""
    specific_property_endpoint = 'https://phoenix.onmap.co.il/v1/properties/'
    params = {'option': '',
              # 'section': 'residence',
              # '$sort': '-is_top_promoted -search_date',
              '$limit': '300',
              '$skip': '0'}

    @classmethod
    def get_properties_ids(cls, buy_or_rent_option: str) -> list:
        """

        :param buy_or_rent_option: can take either the value 'rent' or 'buy'
        :return:
        """
        cls.params['$skip'] = '0'
        cls.params['option'] = buy_or_rent_option

        properties_ids_list = []
        newly_scraped_properties = True

        while newly_scraped_properties:
            response = requests.get(url=cls.onmap_endpoint, params=cls.params)
            data = response.json()['data']

            newly_scraped_properties = [property.get('id') for property in data]
            properties_ids_list.extend(newly_scraped_properties)
            # To scrape the properties that follow
            cls.params['$skip'] = str(int(cls.params['$skip']) + 300)
            #print(cls.params['$skip'])

        cls.save_properties_ids_to_json(buy_or_rent_option=buy_or_rent_option, properties_ids_list=properties_ids_list)
        return properties_ids_list

    @staticmethod
    def save_properties_ids_to_json(buy_or_rent_option: str, properties_ids_list: list, ) -> None:
        """

        :param buy_or_rent_option:
        :param properties_ids_list:
        :return:
        """
        # We would like to save the properties ids in a file for later retrieval
        try:
            with open(config.properties_ids_filepath, 'r') as file:
                existing_properties_ids_dict = json.load(file)
                try:
                    existing_properties_ids = existing_properties_ids_dict[buy_or_rent_option]
                    properties_ids_list = existing_properties_ids + list(
                        set(properties_ids_list) - set(existing_properties_ids))
                except KeyError as ke:
                    print(f'No data for the following key {ke}')

        except FileNotFoundError as fnfe:
            print(f'No file found there: {fnfe}')
            existing_properties_ids_dict = dict()

        existing_properties_ids_dict[buy_or_rent_option] = list(set(properties_ids_list))
        with open(config.properties_ids_filepath, 'w') as file:
            json.dump(existing_properties_ids_dict, file)


def main():
    scraper = Scraper()
    scraper.get_properties_ids(buy_or_rent_option='buy')
    scraper.get_properties_ids(buy_or_rent_option='rent')


if __name__ == '__main__':
    main()
