import csv
import json

def main():
    csvFile = open("datasets/EncuestasSatisfaccionLimpio.csv")
    jsonFile = open("datasets/EncuestasSatisfaccion.json", "w")

    reader = csv.DictReader(csvFile)
    for row in reader:
        del row[""]  # delete the row number
        del row["AreaRecreativaID"]  # delete the reference to AreaRecreativa, it's not needed in mongo

        # transform the numeric values into integers
        row["id"] = row["ID"]
        del row["ID"]

        row["puntuacionAccesibilidad"] = int(row["PUNTUACION_ACCESIBILIDAD"])
        del row["PUNTUACION_ACCESIBILIDAD"]

        row["puntuacionCalidad"] = int(row["PUNTUACION_CALIDAD"])
        del row["PUNTUACION_CALIDAD"]

        row["comentarios"] = row["COMENTARIOS"]
        del row["COMENTARIOS"]

        row["fechaEncuesta"] = row["FECHA"]
        del row["FECHA"]

        json.dump(row, jsonFile)
        jsonFile.write("\n")

if __name__ == "__main__":
    main()
