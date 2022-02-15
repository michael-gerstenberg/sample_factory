from random import randrange
from pymongo import MongoClient
import config
from datetime import datetime
import random

# das datum koennte man noch von anfang bis ende machen pro tool um leichter
# zu querying. Aber auch so geht das mit unwind + sort

# $$$ right now tool and material gets changed at the same time

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]

class RawMaterial:

    # def __init__(self):

    #     self.machine_id = randrange(1, config.quantity_molding_machines+1)
    #     self.machine_status = self.get_machine_status(self.machine_id)

    # if no mat yet, create one

    def create_material_id(self):

        part_type = self.get_random_part()

        db['raw_material'].insert_one({
            "schema": "v1",
            'date': datetime.now(),
            'raw_material_id': self.find_highest_id() + 1,
            'picked_counter': 0,
            'part_quantity': 1000,
            'machine_id': randrange(1, config.quantity_molding_machines+1),
            'type': part_type
        })
        print('Created 1000 pieces of ' + part_type)

    def get_random_part(self):
        parts = config.parts
        return random.choice(parts)

    def find_highest_id(self):
        result = db['raw_material'].find_one({"$query":{},"$orderby":{"raw_material_id":-1}})
        try:
            return result['raw_material_id']
        except:
            return 1

if __name__ == "__main__":
    s = RawMaterial()
    s.create_material_id()
