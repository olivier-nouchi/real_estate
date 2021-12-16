import requests
from urllib.parse import unquote


specific_property_endpoint = 'https://phoenix.onmap.co.il/v1/properties/' # add property id: example: https://phoenix.onmap.co.il/v1/properties/BJOWzFv5K

class Scraper:

    def __init__(self):

        onmap_endpoint = """https://phoenix.onmap.co.il/v1/properties/mixed_search"""
        params = (
            ('option', 'buy'),
            # ('section', 'residence'),
            # ('$sort', '-is_top_promoted -search_date'),
            ('$limit', '300'),
            ('$skip', '0'),
        )

        properties_ids_list = []
        response = requests.get(url=onmap_endpoint, params=params)

        data = response.json()['data']

        for property in data:
            properties_ids_list.append(property.get('id'))

        print(properties_ids_list)
        print(len(properties_ids_list))



scraper = Scraper()