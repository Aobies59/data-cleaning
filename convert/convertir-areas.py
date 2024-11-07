import csv
import json

csvfile = open("./datasets/AreasLimpio.csv")
jsonfile = open("./datasets/AreasLimpio.json", "w")

reader = csv.DictReader(csvfile)
for row in reader:
    # Transformamos la capacidad maxima en numeros
    row["capacidadMAX"] = int(row["capacidadMAX"])

    # Modificamos el incidente de seguridad para que sea una lista y crear el diccionario sea mas sencillo
    incidenteSeguridadArray = row["incidentesSeguridad"][1:-1].split("], ")
    incidenteSeguridadArray = list(filter(lambda x: len(x) > 0, incidenteSeguridadArray))
    cleanIncidenteSeguridadArray = []
    for incidencia in incidenteSeguridadArray:
        incidenciaActualArray = incidencia.split(",")
        for i in range(len(incidenciaActualArray)):
            incidenciaActualArray[i] = incidenciaActualArray[i].strip("[ ']")
        dictToDump = {"id": incidenciaActualArray[0], "fecha": incidenciaActualArray[1], "tipo": incidenciaActualArray[2], "gravedad": incidenciaActualArray[3]}
        cleanIncidenteSeguridadArray.append(dictToDump)
    row["incidentesSeguridad"] = cleanIncidenteSeguridadArray

    # Trasformamos el juego a una lista
    row["Juego"] = list(filter(lambda x: len(x) > 0, row["Juego"][1:-1].split(", ")))

    # Transformamos la cantidad de juegos en una lista y postrriormente cambiamos los elementos de esta por enteros y creamos el diccionario
    row["cantidadJuegosPorTipo"] = list(filter(lambda x: len(x) > 0, row["cantidadJuegosPorTipo"][1:-1].split(", ")))
    for i in range(len(row["cantidadJuegosPorTipo"])):
        row["cantidadJuegosPorTipo"][i] = int(row["cantidadJuegosPorTipo"][i])
    row["cantidadJuegosPorTipo"] = {"DEPORTIVO": row["cantidadJuegosPorTipo"][0], "INFANTIL": row["cantidadJuegosPorTipo"][1], "MAYORES": row["cantidadJuegosPorTipo"][2]}
    row["encuestasSatisfaccion"] = list(filter(lambda x: len(x) > 0, row["encuestasSatisfaccion"][1:-1].split(", ")))

    # Transformamos el registro clima a una lista
    row["RegistroClima"] = list(filter(lambda x: len(x) > 0, row["RegistroClima"][1:-1].split(", ")))

    # Ponemos las coordenadasen una lista y transformamos los strings en floats
    coordenadasArray = row["coordenadasGPS"][1:-1].split(", ")
    row["coordenadasGPS"] = [float(coordenadasArray[0]), float(coordenadasArray[1])]
    
    # Escribimos todo en el json
    json.dump(row, jsonfile, ensure_ascii=False)
    jsonfile.write("\n")