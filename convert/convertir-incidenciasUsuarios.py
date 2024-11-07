import csv
import json
import ast

# Convertir CSV de incidencias de usuarios a JSON
def incidenciasUsuarios_to_json(ruta_csv, ruta_json):
    with open(ruta_csv, encoding='utf-8') as csvFile, open(ruta_json, 'w', encoding='utf-8') as jsonFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            row["id"] = row.pop("ID")
            row["tipoIncidencia"] = row.pop("TIPO_INCIDENCIA")
            row["fechaReporte"] = row.pop("FECHA_REPORTE")
            row["estado"] = row.pop("ESTADO")

            infousuario = []
            for contacto in ast.literal_eval(row.pop("UserInfo")):
                contacts = {
                    "nombre": contacto[0],
                    "email": contacto[1],
                    "telefono": contacto[2]
                }
                infousuario.append(contacts)
            row["Usuario"] = infousuario
            # Borrar inecesarios o ya usados
            del row["UsuarioID"]
            del row["MantenimientoID"]
            #del row["UserInfo"]

            json.dump(row, jsonFile, ensure_ascii=False)
            jsonFile.write('\n')

# Definir rutas de archivos
ruta_csv = "datasets/IncidenciasUsuariosLimpio.csv"
ruta_json = "datasets/IncidenciasUsuarios.json"

def main():
    incidenciasUsuarios_to_json(ruta_csv, ruta_json)

if __name__ == "__main__":
    main()