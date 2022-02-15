from random import randrange
import re
from pymongo import MongoClient
import config
from datetime import datetime

# das datum koennte man noch von anfang bis ende machen pro tool um leichter
# zu querying. Aber auch so geht das mit unwind + sort

# $$$ right now tool and material gets changed at the same time

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]['stations']

result = db.aggregate([
    {
        '$match': {
            'machine_id': 1
        }
    }, {
        '$sort': {
            'date_last_change': -1
        }
    }, {
        '$limit': 1
    }
])

for r in result:
    print(r)


    ----



db.createView(
   "detailedUHUs",
   "UHUs",
   [{$lookup: {
  from: '196p_eucon',
  localField: 'items',
  foreignField: '_id',
  as: 'details'
}}]
)