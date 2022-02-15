from random import randrange
from pymongo import MongoClient
import config
from datetime import datetime

client = MongoClient(config.mongo_connection_string)
coll = client[config.mongo_database]['stations']

class MoldingMachines:

    def equip_all_molding_machines_with_new_tool(self):
        for i in range(1, config.quantity_molding_machines+1):
            self.upsert_tool_info(i)

    def equip_random_molding_machine_with_new_tool(self):
        machine_id = randrange(1, config.quantity_molding_machines+1)
        self.upsert_tool_info(machine_id)

    def upsert_tool_info(self, machine_id, machine_type = "molding"):
        tool_id = randrange(1000,9999)
        material_id = randrange(200000,900000)
        insert = coll.update_one(
            { 
                "machine_id": machine_id, 
                "machine_type": machine_type, 
                "count": { "$lt": 3 } 
            }, { 
                "$push": { 
                    "history": {
                        "type": "changing tool",
                        "tool_id": tool_id,
                        "date": datetime.now(),
                        # 'shots': 0
                    } },
                # "$push": { 
                #     "history": {
                #         "type": "changing material",
                #         "material_id": material_id,
                #         "date": datetime.now(),
                #     } },
                "$inc": { "count": 1 },
                "$set": {
                    "current_tool_id": tool_id,
                    "current_material_id": material_id,
                    "date_tool_changed": datetime.now(),
                    "date_material_changed": datetime.now(),
                    "date_last_change": datetime.now(),
                    # "history.$count"
                },
                # "$min": { "minValue": value, "startDate": datetime.now() },
                # "$max": { "maxValue": value, "endDate": datetime.now() },
                "$setOnInsert": { 
                    "schema": "v1",
                    "machine_id": machine_id, 
                    "machine_type": machine_type,
                    "shots": 0
                }
            },
            upsert=True)

if __name__ == "__main__":
    s = MoldingMachines()
    s.equip_all_molding_machines_with_new_tool()
    # s.equip_random_molding_machine_with_new_tool()
    print(s)