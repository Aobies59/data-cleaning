import csv
import json


csvfile = open("./datasets/meteo_limpio.csv")
jsonfile = open("./datasets/meteo_limpio.json", "w")

reader = csv.DictReader(csvfile)
for row in reader:
    row["id"] = row["ID"]
    del(row["ID"])

    row["fecha"] = row["FECHA"]
    del(row["FECHA"])

    row["temperatura"] = float(row["TEMPERATURA"])
    del(row["TEMPERATURA"])

    row["precipitacion"] = float(row["PRECIPITACION"])
    del(row["PRECIPITACION"])

    row["vientosFuertes"] = row["V_VIENTO"] == "True"

    del(row["V_VIENTO"])

    del(row["CODIGO_POSTAL"])

    del(row["PUNTO_MUESTREO"])

    json.dump(row, jsonfile)
    jsonfile.write("\n")