from random import randrange
from pymongo import MongoClient
import config
from datetime import datetime
import time

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]

class Palette:
    def __init__(self):
        self.palette = self.find_highest_id()
        self.doc = {
            "schema": "v1",
            'palette': self.palette,
            # 'fully_packed': False,
            # 'item_count': 0,
            # 'items': [],
        }
        self.pack_item()

    def find_highest_id(self):
        result = db['palettes'].find_one({"$query":{},"$orderby":{"palette":-1}})
        try:
            if result['item_count'] < 151:
                return result['palette']
            else:
                return result['palette'] + 1
        except:
            return 1
    
    def pack_item(self):
        part_id = self.pick_part()
        db['palettes'].update_one(
        { 
            'palette': self.palette
        }, { 
            "$push": { 
                "items": part_id },
            "$inc": { "item_count": 1 },
            "$setOnInsert": self.doc
        },
        upsert=True)

    def count_available_parts(self):
        return db['final_products'].count_documents({'picked': False})

    def pick_part(self):
        while self.count_available_parts() < 1:
            print('No Items for packing available')
            time.sleep(3)
        part = db['final_products'].find_one_and_update({
                'picked': False
            },{
                '$set': {
                    'picked': True
                }
            })
        return part['_id']

if __name__ == "__main__":
    for _ in range(2000):
        print('Packed a plane on the palette')
        s = Palette()
        # time.sleep(5)