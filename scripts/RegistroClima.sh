#!/bin/sh
python3 clean/limpiar-meteo.py
python3 convert/convertir-meteo.py
mongoimport --db=practica_1-2 --collection=RegistroClimaTemp datasets/meteo_limpio.json
mongosh << EOF
use practica_1-2;
db.RegistroClima.drop();
db.createCollection("RegistroClima", {validator: {\$jsonSchema: {bsonType: "object", title: "Validador de clima", required: ["id", "fecha", "temperatura", "precipitacion", "vientosFuertes"], properties: {id: {bsonType: "string", description: "Id del RegistroClima. Es obligatorio y debe ser un string"}, fecha: {bsonType: "date", description: "Fecha en la que se produjo el RegistroClima. Es obligatorio y debe ser una fecha"}, temperatura: {bsonType: "double", description: "Valor de temperatura medido en el RegistroClima. Es obligatorio y de tipo double"}, precipitacion: {bsonType: "double", description: "Valor de precipitacion medido en el RegistroClima. Es obligatorio y de tipo double"}, vientosFuertes: {bsonType: "bool", description: "True si se han medido vientos fuertes y sino False en el RegistroClima. Es obligatorio y de tipo bool"}}}}});
db.RegistroClima.createIndex({id:1}, {unique:true});
db.RegistroClimaTemp.aggregate([ { \$addFields: { fecha: { \$dateFromString: { dateString: "\$fecha", format: "%d-%m-%Y" } } } }, {\$project: {_id: 0}}, { \$merge: { into: "RegistroClima" } }] );
db.RegistroClimaTemp.drop();
