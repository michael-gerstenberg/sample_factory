from pymongo import MongoClient
import config

client = MongoClient(config.mongo_connection_string)
db = client[config.mongo_database]

if __name__ == "__main__":

    db.create_collection(
        "equipment_history",
        timeseries = {
            "timeField": "timestamp",
            "metaField": "metadata",
            "granularity": "minutes"
        })
