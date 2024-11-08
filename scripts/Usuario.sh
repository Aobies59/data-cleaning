#!/bin/sh
python3 clean/limpiar-usuarios.py
python3 convert/convertir-usuarios.py
mongosh << EOF
use practica_1-2
db.Usuario.drop();
db.createCollection("Usuario", { validator: {\$jsonSchema: { bsonType: "object", title: "Validador de usuarios", required: ["NIF", "nombre", "email", "telefono"], properties: { NIF: { bsonType: "string", description: "El Número de Identificación Fiscal del usuario, es obligatorio y debe ser un string" },  nombre: { bsonType: "string", description: "El nombre del usuario, es obligatorio y debe ser un string" }, email: { bsonType: "string", description: "La dirección de correo electrónico del usuario, es obligatoria y debe ser un string" }, telefono: { bsonType: "string", description: "El número de teléfono del usuario, es obligatorio y debe ser un string" } } }} });
db.Usuario.createIndex({"NIF": 1}, {unique: true});
EOF
mongoimport --host localhost --db=practica_1-2 --collection=Usuario datasets/Usuarios.json
