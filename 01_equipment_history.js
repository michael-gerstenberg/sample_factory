exports = async function(changeEvent) {

  const fullDocument = changeEvent.fullDocument;  
  const eColl = context.services.get("Claschda").db("sample_manufacturing").collection("equipment_history");

  const updateDescription = changeEvent.updateDescription;

  // if (Number.isInteger(updateDescription.updatedFields.shots)){
  //   const shots = updateDescription.updatedFields.shots;
  // } else {
  //   const shots = 0;
  // }

  const insertEnd = eColl.insertOne(
    {
      'timestamp': new Date(),
      'metadata':{
          'machine_id':fullDocument.machine_id
      },  
      "event": "removal",
      "tool_id": updateDescription.updatedFields.current_tool_id,
      "shots": 0
    });

  const insertStart = eColl.insertOne(
    {
      'timestamp': new Date(),
      'metadata':{
          'machine_id':fullDocument.machine_id
      },  
      "event": "mounting",
      "tool_id": fullDocument.current_tool_id,
      "shots": 0
    });
    
}
