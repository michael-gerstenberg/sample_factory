from random import randrange
from pymongo import MongoClient
import config
from datetime import datetime
import time
import random

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]

def get_random_part():
    return random.choice(config.parts)

sample_documents = db['final_products'].aggregate([
    { "$sample": { "size": 2 } }
])

for s in sample_documents:
    part_type = get_random_part()
    db['final_products'].update_one(
    { 
        '_id': s['_id']
    }, {
        "$push": { 
            "nio_parts": {
                'part_type': part_type,
                'timestamp': datetime.now(),
                'raw_material_id': s['parts'][part_type]['raw_material_id']
            }
        },
    })