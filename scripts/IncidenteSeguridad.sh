python3 clean/limpiar-incidentes.py
python3 convert/limpiar-incidentes.py
mongoimport --db=practica_1-2 --collection=IncidenteSeguridadTemp datasets/IncidentesSeguridad.json
mongosh << EOF
db.createCollection("IncidenteSeguridad", {validator: {\$jsonSchema: {bsonType: "object", title: "Validador de IncidenteSeguridad", required: ["id", "fecha", "tipo", "gravedad"], properties: {id: {bsonType: "string", description: "Id del incidente referenciado. Es obligatorio y debe ser un string"}, fecha: {bsonType: "date", description: "Fecha en la que se produjo el incidente. Es obligatorio y debe ser una fecha"}, tipo: {bsonType: "string", enum: ["Robo", "Caída", "Accidente", "Vandalismo", "Daño estructural"], description: "Tipo de incidente de seguridad. Debe ser Robo o Caída o Accidente o Vandalismo o Daño estructural"}, gravedad: {bsonType: "string", enum: ["Alta", "Baja", "Crítica", "Media"], description: "Gravedad del incidente de seguridad. Debe ser Alta o Baja o Crítica o Media"}}}});
db.IncidenteSeguridad.createIndex({id:1}, {required:true});
db.IncidenteSeguridadTemp.aggregate([{\$addFields: {fecha: {\$dateFromString: {dateString: "\$fecha", format: "%d-%m-%Y"}}}}, {\$project: {_id: 0}}, {\$merge: {into: "IncidenteSeguridad"}}]);
