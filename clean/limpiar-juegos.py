import math
import pandas as pd
import numpy as np
from random import randint

from pandas.util.version import Infinity

def dateOccursLater(date1, date2):
    date1Elements = date1.split("-")
    if len(date1Elements) != 3:
        return True
    for currElement in date1Elements:
        if not currElement.isdigit():
            return True
    date1Day = int(date1Elements[0])
    date1Month = int(date1Elements[1])
    date1Year = int(date1Elements[2])

    date2Elements = date2.split("-")
    if len(date2Elements) != 3:
        return False
    for currElement in date2Elements:
        if not currElement.isdigit():
            return True
    date2Day = int(date2Elements[0])
    date2Month = int(date2Elements[1])
    date2Year = int(date2Elements[2])

    if date2Year > date1Year:
        return True
    elif date2Year < date1Year:
        return False

    if date2Month > date1Month:
        return True
    elif date2Month < date1Year:
        return False

    if date2Day > date1Day:
        return True
    else:
        return False

def main():
    juegos = pd.read_csv("datasets/JuegosSucio.csv")

    # eliminar IDs duplicados
    previousIds = set({})
    for i, currJuego in juegos.iterrows():
        if currJuego["ID"] in previousIds:
            juegos.drop(i, inplace=True)
        else:
            previousIds.add(currJuego["ID"])

    # cambiar el formato de FECHA_INSTALACION
    defaultDate = "01-01-1996"  # misma fecha por defecto que AreaRecreativa
    for i, currJuego in juegos.iterrows():
        currDate: str = str(currJuego["FECHA_INSTALACION"])[:10]
        currDate = currDate.replace("/", "-")
        currDateSplit = currDate.split("-")
        if len(currDateSplit) != 3:
            juegos.at[i, "FECHA_INSTALACION"] = defaultDate
            continue
        for currDateSplitElement in currDateSplit:
            if not currDateSplitElement.isdigit():
                juegos.at[i, "FECHA_INSTALACION"] = defaultDate
                continue

        day:str = ""
        month:str = ""
        year:str = ""
        if len(currDateSplit[0]) == 4:
            year = currDateSplit[0]
            if int(currDateSplit[1]) > 12:
                day = currDateSplit[1]
                month = currDateSplit[2]
            else:
                day = currDateSplit[2]
                month = currDateSplit[1]
        elif len(currDateSplit[1]) == 4:  # wtf
            year = currDateSplit[1]
            if int(currDateSplit[2]) > 12:
                day = currDateSplit[2]
                month = currDateSplit[0]
            else:
                day = currDateSplit[0]
                month = currDateSplit[2]
        elif len(currDateSplit[2]) == 4:
            year = currDateSplit[2]
            if int(currDateSplit[1]) > 12:
                day = currDateSplit[1]
                month = currDateSplit[0]
            else:
                day = currDateSplit[0]
                month = currDateSplit[1]
        else:
            day = currDateSplit[0]
            month = currDateSplit[1]
            year = currDateSplit[2]
            if int(year) <= 24:
                year = f"20{year}"
            else:
                year = f"19{year}"

        currUpdatedDate = f"{day}-{month}-{year}"
        juegos.at[i, "FECHA_INSTALACION"] = currUpdatedDate

    # convertir ACCESIBLE en booleanos
    juegos["ACCESIBLE"] = juegos["ACCESIBLE"].astype(bool)

    # cambiar el formato de TIPO
    juegos["TIPO"] = juegos["tipo_juego"]
    juegos.loc[juegos["TIPO"] == "deportivas", "TIPO"] = "DEPORTIVO"
    juegos.loc[juegos["TIPO"] == "infantiles", "TIPO"] = "INFANTIL"
    juegos.loc[juegos["TIPO"] == "mayores", "TIPO"] = "MAYORES"

    # añadir referencias a MANTENIMIENTOS y a ULTIMA_FECHA_MANTENIMIENTO
    juegos["MANTENIMIENTOS"] = [[] for _ in range(len(juegos))]
    juegos["ULTIMA_FECHA_MANTENIMIENTO"] = ["" for _ in range(len(juegos))]
    mantenimientos = pd.read_csv("datasets/MantenimientoLimpio.csv")
    for i, currJuego in juegos.iterrows():
        latestDate = currJuego["FECHA_INSTALACION"]
        for currFecha in list(mantenimientos.loc[mantenimientos["JuegoID"] == currJuego["ID"], "FECHA_INTERVENCION"]):
            if dateOccursLater(latestDate, currFecha):
                latestDate = currFecha
        juegos.at[i, "ULTIMA_FECHA_MANTENIMIENTO"] = latestDate


        mantenimientosIds = list(mantenimientos.loc[mantenimientos["JuegoID"] == currJuego["ID"], "ID"])
        juegos.at[i, "MANTENIMIENTOS"] = mantenimientosIds

    # añadir referencias tipo resumen a INCIDENCIAS
    # resumen: [id, tipo, fecha, estado]
    juegos["INCIDENCIAS"] = [[] for _ in range(len(juegos))]
    incidencias = pd.read_csv("datasets/IncidenciasUsuariosLimpio.csv")
    mantenimientoDict = {}  # diccionario con forma MantenimientoID: [Resúmenes de incidencias]
    for i, currIncidencia in incidencias.iterrows():
        # por algún motivo las incidencias no se pueden leer como un array
        mantenimientoIds = [int(currId.strip().strip('""').strip("''")) for currId in str(currIncidencia["MantenimientoID"]).strip("[]").split(",")]
        for currMantenimientoID in mantenimientoIds:
            if mantenimientoDict.get(currMantenimientoID) is None:
                mantenimientoDict[currMantenimientoID] = []
            mantenimientoDict[currMantenimientoID].append([int(currIncidencia["ID"]), currIncidencia["TIPO_INCIDENCIA"], currIncidencia["FECHA_REPORTE"], currIncidencia["ESTADO"]])

    for i, currJuego in juegos.iterrows():
        currIncidencias = []
        for currMantenimientoId in currJuego["MANTENIMIENTOS"]:
            incidenciasReference = mantenimientoDict.get(currMantenimientoId)
            if incidenciasReference is not None:
                currIncidencias.extend(mantenimientoDict[currMantenimientoId])

        juegos.at[i, "INCIDENCIAS"] = currIncidencias

    # añadir desgaste acumulado
    juegos["DESGASTE_ACUMULADO"] = [0 for _ in range(len(juegos))]
    for i, currJuego in juegos.iterrows():
        juegos.at[i, "DESGASTE_ACUMULADO"] = len(currJuego["MANTENIMIENTOS"])

    # como la columna de INDICADOR_EXPOSICION no está presente, rellenamos aleatoriamente con {Bajo, Medio, Alto}
    possibleIndicators = ["Bajo", "Medio", "Alto"]
    juegos["INDICADOR_EXPOSICION"] = [possibleIndicators[randint(0, 2)] for _ in range(len(juegos))]

    # como la columna de NOMBRE no está presente, rellenamos con JUEGO-<ID>
    juegos["NOMBRE"] = ["" for _ in range(len(juegos))]
    for i, currJuego in juegos.iterrows():
        juegos.at[i, "NOMBRE"] = f"JUEGO-{currJuego['ID']}"

    # usamos las coordenadas para asignarle a cada juego el área más cercana
    areas = pd.read_csv("datasets/AreasSucio.csv")
    juegos["AreaID"] = ["" for _ in range(len(juegos))]
    for i, currJuego in juegos.iterrows():
        closestAreaID = None
        closestAreaDistance = Infinity
        for j, currArea in areas.iterrows():
            currDistance = math.sqrt((currArea["COORD_GIS_X"] - currJuego["COORD_GIS_X"]) ** 2 + (currArea["COORD_GIS_Y"] - currArea["COORD_GIS_Y"]) ** 2)
            if currDistance < closestAreaDistance:
                closestAreaID = currArea["ID"]
                closestAreaDistance = currDistance
        juegos.at[i, "AreaID"] = closestAreaID

    # eliminar columnas innecesarias
    columnsToDrop = ["tipo_juego", "DESC_CLASIFICACION", "COD_BARRIO", "COD_DISTRITO", "DISTRITO", "BARRIO", "COORD_GIS_X", "COORD_GIS_Y", "SISTEMA_COORD",
        "LATITUD", "LONGITUD", "TIPO_VIA", "NOM_VIA", "NUM_VIA", "COD_POSTAL", "DIRECCION_AUX", "NDP", "CONTRATO_COD", "CODIGO_INTERNO"]

    for currColumn in columnsToDrop:
        juegos = juegos.drop(currColumn, axis=1)

    juegos.to_csv("datasets/JuegosLimpio.csv")

if __name__ == "__main__":
    main()
