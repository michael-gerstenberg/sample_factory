
db.createView(
   "useCase3",
   "final_products",

[{
    $match: {
        nio_parts: {
            $exists: true
        }
    }
}, {
    $unwind: '$nio_parts'
}, {
    $project: {
        _id: 1,
        serialnumber: 1,
        timestamp_assembled: '$timestamp',
        picked: 1,
        part_type: '$nio_parts.part_type',
        timestamp_nio: '$nio_parts.timestamp',
        raw_material_id: '$nio_parts.raw_material_id'
    }
}, {
    $group: {
        _id: '$raw_material_id',
        nio_parts: {
            $addToSet: {
                _id: '$_id',
                serialnumber: '$serialnumber',
                picked: '$picked',
                timestamp_assembled: '$timestamp_assembled',
                part_type: '$part_type',
                timestamp_nio: '$timestamp_nio'
            }
        }
    }
}, {
    $project: {
        _id: 0,
        nio_parts: 1,
        raw_material_id: '$_id'
    }
}]

)