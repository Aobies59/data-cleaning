#!/bin/sh
python3 clean/limpiar-encuestas.py
python3 convert/convertir-encuestas.py
mongoimport --host localhost --db=practica_1-2 --collection=EncuestaSatisfaccionTemp datasets/EncuestasSatisfaccion.json
mongosh << EOF
use practica_1-2
db.EncuestaSatisfaccion.drop();
db.createCollection("EncuestaSatisfaccion", {validator: {\$jsonSchema: {bsonType: "object", title: "Validador de encuestas de satisfacción", required: ["id", "fechaEncuesta", "puntuacionAccesibilidad", "puntuacionCalidad", "comentarios"] , properties: {id: {bsonType: "string", description: "id de la encuesta de satisfacción, es obligatorio y debe ser un string"}, fechaEncuesta: {bsonType: "date", description: "Fecha de realización de la encuesta de satisfacción, es obligatoria y debe ser una fecha"}, puntuacionAccesibilidad: {bsonType: "int", description: "Puntuación de accesibilidad recibida en la encuesta de satisfacción. Debe ser un entero y es obligatorio"}, puntuacionCalidad: {bsonType: "int", description: "Puntuación de calidad recibida en la encuesta de satisfacción. Debe ser un entero y es obligatorio."},comentarios: {bsonType: "string", description: "Comentarios recibidos en la encuesta de satisfacción. Debe ser un string y es obligatorio"}  }}}});
db.EncuestaSatisfaccion.createIndex({id:1}, {unique:true});
db.EncuestaSatisfaccionTemp.aggregate([{ \$addFields: { fechaEncuesta: { \$dateFromString: { dateString: "\$fechaEncuesta", format: "%d-%m-%Y" } } } },{\$project: {_id: 0}}, { \$merge: { into: "EncuestaSatisfaccion", on: "id", whenMatched: "merge" } }]);
db.EncuestaSatisfaccionTemp.drop();
