python3 clean/limpiar-incidentes.py
python3 convert/convertir-incidentes.py
mongoimport --db=practica_1-2 --collection=IncidenteSeguridadTemp datasets/IncidentesSeguridad.json
mongosh << EOF
use practica_1-2
db.IncidenteSeguridad.drop();
db.createCollection("IncidenteSeguridad", {validator: {\$jsonSchema: {bsonType: "object", title: "Validador de IncidenteSeguridad", required: ["id", "fechaReporte", "tipoIncidente", "gravedad"], properties: {id: {bsonType: "string", description: "Id del incidente referenciado. Es obligatorio y debe ser un string"}, fechaReporte: {bsonType: "date", description: "Fecha en la que se produjo el incidente. Es obligatorio y debe ser una fecha"}, tipoIncidente: {bsonType: "string", enum: ["Robo", "Caída", "Accidente", "Vandalismo", "Daño estructural"], description: "Tipo de incidente de seguridad. Debe ser Robo o Caída o Accidente o Vandalismo o Daño estructural"}, gravedad: {bsonType: "string", enum: ["Alta", "Baja", "Crítica", "Media"], description: "Gravedad del incidente de seguridad. Debe ser Alta o Baja o Crítica o Media"}}}}});
db.IncidenteSeguridad.createIndex({id:1}, {required:true});
db.IncidenteSeguridadTemp.aggregate([{\$addFields: {fechaReporte: {\$dateFromString: {dateString: "\$fechaReporte", format: "%d-%m-%Y"}}}}, {\$project: {_id: 0}}, {\$merge: {into: "IncidenteSeguridad"}}]);
