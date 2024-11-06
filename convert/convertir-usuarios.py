import csv
import json

def main():
    csvFile = open("datasets/UsuariosLimpio.csv")
    jsonFile = open("datasets/Usuarios.json", "w")

    reader = csv.DictReader(csvFile)
    for row in reader:
        del row[""]  # field with the row number

        row["nombre"] = row["NOMBRE"]
        del row["NOMBRE"]

        row["email"] = row["EMAIL"]
        del row["EMAIL"]

        row["telefono"] = row["TELEFONO"]
        del row["TELEFONO"]

        json.dump(row, jsonFile)
        jsonFile.write("\n")

if __name__ == "__main__":
    main()
