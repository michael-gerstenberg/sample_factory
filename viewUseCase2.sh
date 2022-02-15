db.createView(
   "useCase2",
   "palettes",
    [{$lookup: {
 from: 'final_products',
 localField: 'items',
 foreignField: '_id',
 as: 'details'
}}, {$project: {
 _id: 0,
 palette: 1,
 details: 1
}}, {$unwind: '$details'}, {$project: {
 palette: 1,
 serialnumber: '$details.serialnumber',
 parts: {
  $objectToArray: '$details.parts'
 }
}}, {$unwind: '$parts'}, {$project: {
 palette: 1,
 serialnumber: 1,
 partType: '$parts.k',
 productionDate: '$parts.v.date',
 raw_material_id: '$parts.v.raw_material_id',
 machineId: '$parts.v.machine_id',
 materialId: '$parts.v.material_id',
 toolId: '$parts.v.tool_id'
}}, {$group: {
 _id: '$raw_material_id',
 palettes: {
  $addToSet: '$palette'
 }
}}, {$project: {
 _id: 0,
 palettes: 1,
 raw_material_id: '$_id'
}}]
)