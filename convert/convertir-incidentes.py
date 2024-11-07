import csv
import json


csvfile = open("./datasets/IncidentesSeguridadLimpio.csv")
jsonfile = open("./datasets/IncidentesSeguridad.json", "w")

reader = csv.DictReader(csvfile)
for row in reader:
    # Solo debemos renombrar las columnas para que estas tengan el formato adecuado
    row["id"] = row["ID"]
    del(row["ID"])

    row["fechaReporte"] = row["FECHA_REPORTE"]
    del(row["FECHA_REPORTE"])

    row["tipoIncidente"] = row["TIPO_INCIDENTE"]
    del(row["TIPO_INCIDENTE"])

    row["gravedad"] = row["GRAVEDAD"]
    del(row["GRAVEDAD"])

    del(row["AreaRecreativaID"])

    json.dump(row, jsonfile, ensure_ascii=False)
    jsonfile.write("\n")
