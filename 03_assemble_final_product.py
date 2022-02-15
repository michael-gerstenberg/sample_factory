from random import randrange
from pymongo import MongoClient
import config
from datetime import date, datetime
import time
import random

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]

class FinalProduct:

    def __init__(self):
        self.serialnumber = self.find_highest_id() + 1
        self.doc = {
            "schema": "v1",
            'serialnumber': self.serialnumber,
            'timestamp': datetime.now(),
            'picked': False,
            'parts': {
                'wheel': self.pick_raw_material('wheel'),
                'brezel': self.pick_raw_material('brezel'),
                'windshield': self.pick_raw_material('windshield'),
                'wing': self.pick_raw_material('wing'),
                'body': self.pick_raw_material('body'),
            }
        }
        self.insert()

    def find_highest_id(self):
        result = db['final_products'].find_one({"$query":{},"$orderby":{"serialnumber":-1}})
        try:
            return result['serialnumber']
        except:
            return 1

    def count_available_mat(self, part_type):
        count = db['raw_material'].count_documents({
                    'picked_counter': {
                        '$lt': 1000
                    },
                    'type': part_type})
        return count

    def pick_raw_material(self, part_type):
    
        while self.count_available_mat(part_type) < 1:
            print('No ' + part_type + ' material available. Waiting 5s.')
            time.sleep(5)

        available_raw_material = db['raw_material'].aggregate([
            {
                '$match': {
                    'picked_counter': {
                        '$lt': 1000
                    },
                    'type': part_type
                }
            }, {
                '$sort': {
                    'date': 1
                }
            }, {
                '$limit': 1
            }, {
                '$project': { 
                    '_id': 0,
                    'picked_counter': 0,
                    'part_quantity': 0
                }
            }
        ])
        for r in available_raw_material:
            self.update_to_used_raw_material(r["raw_material_id"])
            return r

    def update_to_used_raw_material(self, raw_material_id):
        update = db['raw_material'].update_one({
            "raw_material_id": raw_material_id
        },{
            "$inc": { "picked_counter": 1 },
        })


    def insert(self):
        db['final_products'].insert_one(self.doc)


if __name__ == "__main__":

    for _ in range(1000):
        s = FinalProduct()
        print('New Part assembled')
        
        # time.sleep(random.random())