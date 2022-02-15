exports = async function(changeEvent) {

    const fullDocument = changeEvent.fullDocument;
    
    const stationCollection = context.services.get("Claschda").db("sample_manufacturing").collection("stations");
    const matCollection = context.services.get("Claschda").db("sample_manufacturing").collection("raw_material");
  
    const doc = await stationCollection.findOne({
      'machine_id': fullDocument['machine_id']
      });
    
    str = JSON.stringify(doc);
  
    console.log(str)
    
    const update = matCollection.updateOne(
      {
        "raw_material_id": fullDocument.raw_material_id
      },{
        "$set": {
          "material_id": doc.current_material_id,
          "tool_id": doc.current_tool_id
          // "tool_id": doc
        }
      });
  
  };
    
    
    