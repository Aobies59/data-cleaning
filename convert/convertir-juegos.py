import csv
import json

def main():
    csvFile = open("datasets/JuegosLimpio.csv")
    jsonFile = open("datasets/Juegos.json", "w")

    reader = csv.DictReader(csvFile)
    for row in reader:
        del row[""]
        del row["AreaID"]

        row["id"] = row["ID"]
        del row["ID"]

        row["modelo"] = row["MODELO"]
        del row["MODELO"]

        row["estadoOperativo"] = row["ESTADO"]
        del row["ESTADO"]

        row["accesibilidad"] = True if row["ACCESIBLE"] == "True" else False
        del row["ACCESIBLE"]

        row["fechaInstalacion"] = row["FECHA_INSTALACION"]
        del row["FECHA_INSTALACION"]

        row["tipo"] = row["TIPO"]
        del row["TIPO"]

        row["desgasteAcumulado"] = int(row["DESGASTE_ACUMULADO"])
        del row["DESGASTE_ACUMULADO"]

        incidenciasArray = row["INCIDENCIAS"][1:-1].split("],")
        incidenciasArray = list(filter(lambda x: len(x) > 0, incidenciasArray))
        cleanIncidenciasArray = []
        for currIncidencia in incidenciasArray:
            currIncidenciaArray = currIncidencia.split(",")
            for i in range(len(currIncidenciaArray)):
                currIncidenciaArray[i] = currIncidenciaArray[i].strip(" [']")
            currIncidenciaDict = {"id": currIncidenciaArray[0], "tipoIncidencia": currIncidenciaArray[1], "fechaReporte": currIncidenciaArray[2],
                "estado": currIncidenciaArray[3]}
            cleanIncidenciasArray.append(currIncidenciaDict)
        row["incidencias"] = cleanIncidenciasArray
        del row["INCIDENCIAS"]

        row["mantenimientos"] = list(filter(lambda x: len(x) > 0, [currMantenimiento.strip() for currMantenimiento in row["MANTENIMIENTOS"].strip("[]").split(",")]))
        del row["MANTENIMIENTOS"]

        row["ultimaFechaMantenimiento"] = row["ULTIMA_FECHA_MANTENIMIENTO"]
        del row["ULTIMA_FECHA_MANTENIMIENTO"]

        row["indicadorExposicion"] = row["INDICADOR_EXPOSICION"]
        del row["INDICADOR_EXPOSICION"]

        row["nombre"] = row["NOMBRE"]
        del row["NOMBRE"]

        json.dump(row, jsonFile)
        jsonFile.write("\n")


if __name__ == "__main__":
    main()
