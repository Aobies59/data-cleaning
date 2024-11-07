python3 clean/limpiar-mantenimiento.py
python3 convert/convertir-mantenimiento.py
mongoimport --host localhost --db=practica_1-2 --collection=MantenimientoTemp datasets/Mantenimiento.json
mongosh << EOF
use practica_1-2;
db.Mantenimiento.drop();
db.createCollection("Mantenimiento", { validator: { \$jsonSchema: { "bsonType": "object", "required": ["id", "fechaIntervencion", "tipoIntervencion", "estadoPrevio", "estadoPosterior"], "properties": { "id": { "bsonType": "string", "description": "Debe ser una cadena que identifique el mantenimiento" }, "fechaIntervencion": { "bsonType": "date", "description": "Debe ser una fecha válida en formato ISO (YYYY-MM-DD)" }, "tipoIntervencion": { "bsonType": "string", "enum": ["Correctivo", "Preventivo", "Emergencia"], "description": "Debe ser 'Energencia','Correctivo' o 'Preventivo'" }, "estadoPrevio": { "bsonType": "string", "enum": ["Malo", "Bueno", "Regular"], "description": "Debe ser un estado válido del juego antes del mantenimiento" }, "estadoPosterior": { "bsonType": "string", "enum": ["Malo", "Bueno", "Regular"], "description": "Debe ser un estado válido del juego después del mantenimiento" }, "Comentarios": { "bsonType": "string", "description": "Comentarios opcionales sobre el mantenimiento" } } } } });
db.Mantenimiento.createIndex({id:1}, {unique:true});
db.MantenimientoTemp.aggregate([ { \$addFields: { fechaIntervencion: { \$dateFromString: { dateString: "\$fechaIntervencion", format: "%d-%m-%Y" } } } }, { \$project: { _id: 0 } }, { \$merge: { into: "Mantenimiento", on: "id", whenMatched: "merge" } } ]);
db.MantenimientoTemp.drop();
