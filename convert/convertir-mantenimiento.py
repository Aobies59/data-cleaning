import csv
import json

# Convertir CSV de mantenimiento a JSON
def mantenimiento_to_json(ruta_csv, ruta_json):
    with open(ruta_csv) as csvFile, open(ruta_json, 'w') as jsonFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            row["id"] = row.pop("ID")
            row["fechaIntervencion"] = row.pop("FECHA_INTERVENCION")
            row["tipoIntervencion"] = row.pop("TIPO_INTERVENCION")
            row["estadoPrevio"] = row.pop("ESTADO_PREVIO")
            row["estadoPosterior"] = row.pop("ESTADO_POSTERIOR")
            row["comentarios"] = row.pop("Comentarios")
            del row["JuegoID"] 
            json.dump(row, jsonFile)
            jsonFile.write('\n')

# Definir rutas de archivos
ruta_csv = "datasets/MantenimientoLimpio.csv"
ruta_json = "datasets/Mantenimiento.json"
def main():
    mantenimiento_to_json(ruta_csv, ruta_json)

if __name__ == "__main__":
    main()