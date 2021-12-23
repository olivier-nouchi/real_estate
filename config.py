import os

DATA_DIR_NAME = 'data'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, DATA_DIR_NAME)

properties_ids_filename = 'properties_ids.json'

properties_ids_filepath = os.path.join(DATA_DIR, properties_ids_filename)

#print(bool(os.stat(properties_ids_filepath).st_size))