#!/bin/bash

python3 clean/limpiar-areas.py || { echo "Python script limpiar-areas.py failed"; exit 1; }
python3 convert/convertir-areas.py || { echo "Python script convertir-areas.py failed"; exit 1; }

mongoimport --db=practica_1-2 --collection=AreaRecreativaTemp datasets/Areas.json || { echo "mongoimport failed"; exit 1; }

mongosh << EOF
use practica_1-2;

db.AreaRecreativa.drop();
db.createCollection("AreaRecreativa", {
  validator: {
    \$jsonSchema: {
      bsonType: "object",
      title: "Validador de areas",
      required: ["nombre","estadoOperativo","fechaInstalacion","coordenadasGPS","capacidadMAX","barrio","distrito","incidentesSeguridad","encuestasSatisfaccion","RegistroClima","Juego","cantidadJuegosPorTipo"],
      properties: {
        nombre: { bsonType: "string", description: "Nombre del AreaRecreativa. Es unico, obligatorio y debe ser de tipo string" },
        estadoOperativo: { bsonType: "string", enum: ["OPERATIVO", "NO OPERATIVO"], description: "Estado actual del AreaRecreativa. Es obligatorio y debe ser OPERATIVO o NO OPERATIVO" },
        fechaInstalacion: { bsonType: "date", description: "Fecha de instalación del AreaRecreativa. Es obligatorio y debe ser una fecha" },
        coordenadasGPS: { bsonType: "array", description: "Lista de dos elementos obligatoria con las coordenadas del AreaRecreativa. El formato es [longitud, latitud]", items: { bsonType: "double" } },
        capacidadMAX: { bsonType: "int", description: "Capacidad máxima del AreaRecreativa. Es obligatorio y de tipo entero" },
        barrio: { bsonType: "string", description: "Barrio en el que se encuentra el AreaRecreativa. Es obligatorio y de tipo string" },
        distrito: { bsonType: "string", description: "Distrito en el que se encuentra el AreaRecreativa. Es obligatorio y de tipo string" },
        incidentesSeguridad: { bsonType: "array", description: "Referencia con resumen de todos los incidentes de seguridad producidos en el AreaRecreativa. Es obligatorio y es un array de objetos incidente", items: { title: "incidente", bsonType: "object", required: ["id", "fecha", "tipo", "gravedad"], properties: { id: { bsonType: "string", description: "Id del incidente referenciado. Es obligatorio y debe ser un string" }, fecha: { bsonType: "date", description: "Fecha en la que se produjo el incidente. Es obligatorio y debe ser una fecha" }, tipo: { bsonType: "string", enum: ["Robo", "Caída", "Accidente", "Vandalismo", "Daño estructural"], description: "Tipo de incidente de seguridad. Debe ser 'Robo' o 'Caída' o 'Accidente' o 'Vandalismo' o 'Daño estructural'" }, gravedad: { bsonType: "string", enum: ["Alta", "Baja", "Crítica", "Media"], description: "Gravedad del incidente de seguiridad. Debe ser Alta o Baja o Crítica o Media" } } } },
        encuestasSatisfaccion: { bsonType: "array", description: "Referencia a las encuestas de satisfaccion del AreaRecreativa. Es obligatorio y de tipo array", items: { bsonType: "string" } },
        RegistroClima: { bsonType: "array", description: "Referencia a los registros del clima que afectan al AreaRecreativa. Es obligatorio y de tipo array", items: { bsonType: "string" } },
        Juego: { bsonType: "array", description: "Referencia a las encuestas de satisfaccion del AreaRecreativa. Es obligatorio y de tipo array", items: { bsonType: "string" } },
        cantidadJuegosPorTipo: { bsonType: "object", required: ["DEPORTIVO", "INFANTIL", "MAYORES"], properties: { DEPORTIVO: { bsonType: "int", description: "Número de juegos de tipo DEPORTIVO en el AreaRecreativa" }, INFANTIL: { bsonType: "int", description: "Número de juegos de tipo INFANTIL en el AreaRecreativa" }, MAYORES: { bsonType: "int", description: "Número de juegos de tipo MAYORES en el AreaRecreativa" } } }
      }
    }
  }
});

db.AreaRecreativa.createIndex({nombre: 1}, {unique: true});

db.AreaRecreativaTemp.aggregate([
  { \$addFields: { 
    fechaInstalacion: { \$dateFromString: { dateString: "\$fechaInstalacion", format: "%d-%m-%Y" } }, 
    incidentesSeguridad: { 
      \$map: { 
        input: "\$incidentesSeguridad", 
        as: "incidentesSeguridad", 
        in: { 
          \$mergeObjects: [ 
            "\$\$incidentesSeguridad", 
            { fechaReporte: { \$dateFromString: { dateString: "\$\$incidentesSeguridad.fecha", format: "%d-%m-%Y" } } } 
          ] 
        } 
      } 
    } 
  }},
  { \$project: { _id: 0 } },
  { \$merge: { into: "AreaRecreativa" } }
]);

db.AreaRecreativaTemp.drop();

EOF
