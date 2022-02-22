from collections import namedtuple
from utils import format_datetime


class FeatureExtractor:

    def __init__(self, properties):
        self.raw_properties_info = properties

    def parsing_raw_property_info(self):
        """

        :return:
        """

        clean_properties = {}

        for property in self.raw_properties_info:
            property_id = property

            data = self.raw_properties_info[property_id]
            property_desc = data.get('description')
            property_is_active = data.get('is_active')
            property_has_photos = data.get('has_photos')

            additional_info = data.get('additional_info')
            property_has_basement = additional_info.get('hasBasement')
            property_bathrooms = additional_info.get('bathrooms')
            property_toilets = additional_info.get('bathrooms')
            property_elevators = additional_info.get('elevators')
            property_balconies = additional_info.get('balconies')

            property_entry = additional_info.get('entry_date')
            property_entry_date = property_entry.get('date')
            property_entry_immediate = property_entry.get('immediate')
            property_entry_flexible = property_entry.get('flexible')

            property_construction_year = additional_info.get('construction_year')
            property_light_direction_four = additional_info.get('construction_year')
            property_light_direction = [bool(direction) for direction in
                                        property_light_direction_four]  # NESO encoded in one hot

            property_rooms = additional_info.get('rooms')
            property_floor = additional_info.get('floor')
            property_floor_on_the = property_floor.get('on_the')
            property_floor_out_of = property_floor.get('out_of')

            property_area = additional_info.get('area')
            property_area_garden = property_area.get('garden')
            property_area_field = property_area.get('field')
            property_area_base = property_area.get('base')

            property_parking = additional_info.get('parking')
            property_parking_aboveground = property_area.get('aboveground')
            property_parking_underground = property_area.get('underground')

            property_price = additional_info.get('price')
            property_section = additional_info.get('section')
            property_search_option = additional_info.get('search_option')
            property_type = additional_info.get('property_type')
            property_num_images = len(additional_info.get('images'))

            property_address = additional_info.get('address')
            property_address_tags = property_address.get('tags')
            property_tag_address = namedtuple("address_tags", "city street number")
            property_tag_address.city = property_address_tags[0] if 0 < len(property_tag_address) else None
            property_tag_address.street = property_address_tags[1] if 1 < len(property_tag_address) else None
            property_tag_address.number = property_address_tags[2] if 2 < len(property_tag_address) else None
            property_address_location = property_address.get('location')
            property_address_location_lat = property_address_location.get('lat')
            property_address_location_long = property_address_location.get('long')
            property_address_en = property_address.get('en')
            property_address_city_name = property_address_en.get('city_name')
            property_address_house_number = property_address_en.get('house_number')
            property_address_street_name = property_address_en.get('street_name')
            property_address_neighborhood = property_address_en.get('neighborhood')
            property_place_id = property_address.get('place_id')

            property_commodities = additional_info.get('commodities')
            property_has_videos = additional_info.get('videos')
            property_search_date = format_datetime(additional_info.get('search_date'))
            property_created_at = format_datetime(additional_info.get('created_at'))
            property_updated_at = format_datetime(additional_info.get('updated_at'))
            property_scraping_date = property.get('scraping_date')

            property_attributes = {property_id:
                                       {'property_desc': property_desc,
                                        'property_is_active': property_is_active,
                                        'property_has_photos': property_has_photos,
                                        'property_has_basement': property_has_basement,
                                        'property_bathrooms': property_bathrooms,
                                        'property_toilets': property_toilets,
                                        'property_elevators': property_elevators,
                                        'property_balconies': property_balconies,
                                        'property_entry_date': property_entry_date,
                                        'property_entry_immediate': property_entry_immediate,
                                        'property_entry_flexible': property_entry_flexible,
                                        'property_construction_year': property_construction_year,
                                        'property_light_direction': property_light_direction,
                                        'property_rooms': property_rooms,
                                        'property_floor_on_the': property_floor_on_the,
                                        'property_floor_out_of': property_floor_out_of,
                                        'property_area_garden': property_area_garden,
                                        'property_area_field': property_area_field,
                                        'property_area_base': property_area_base,
                                        'property_parking': property_parking,
                                        'property_parking_aboveground': property_parking_aboveground,
                                        'property_parking_underground': property_parking_underground,
                                        'property_price': property_price,
                                        'property_section': property_section,
                                        'property_search_option': property_search_option,
                                        'property_type': property_type,
                                        'property_num_images': property_num_images,
                                        'property_tag_address': property_tag_address
                                        'property_address_location_lat': property_address_location_lat,
                                        'property_address_location_long': property_address_location_long,
                                        'property_address_city_name': property_address_city_name,
                                        'property_address_house_number': property_address_house_number,
                                        'property_address_street_name': property_address_street_name,
                                        'property_address_neighborhood': property_address_neighborhood,
                                        'property_place_id': property_place_id,
                                        'property_commodities': property_commodities,
                                        'property_has_videos': property_has_videos,
                                        'property_search_date': property_search_date,
                                        'property_created_at': property_created_at,
                                        'property_updated_at': property_updated_at,
                                        'property_scraping_date': property_scraping_date
                                        }
                                   }

        clean_properties = clean_properties.update(property_attributes)

        return clean_properties