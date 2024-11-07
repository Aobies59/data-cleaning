import pandas as pd
import csv
import json


df = pd.read_csv("./datasets/IncidentesSeguridadSucio.csv")


#%% ---LIMPIEZA TIPO_ACCIDENTE---
"""
Solo debemos eliminar las instancias incorrectas de cada uno de los tipos de accidentes.
Para saber todos los tipos de accidentes diferentes se hace: print(df['TIPO_INCIDENTE'].unique())
"""

for index, row in df.iterrows():
    if row["TIPO_INCIDENTE"] == "Accídénté":
        df.loc[index, "TIPO_INCIDENTE"] = "Accidente"

    elif row["TIPO_INCIDENTE"] == "Cáídá":
        df.loc[index, "TIPO_INCIDENTE"] = "Caída"

    elif row["TIPO_INCIDENTE"] == "Dáñó éstrúctúrál":
        df.loc[index, "TIPO_INCIDENTE"] = "Daño estructural"

    elif row["TIPO_INCIDENTE"] == "Vándálísmó":
        df.loc[index, "TIPO_INCIDENTE"] = "Vandalismo"

    elif row["TIPO_INCIDENTE"] == "Róbó":
        df.loc[index, "TIPO_INCIDENTE"] = "Robo"

    


#%% ---LIMPIEZA FECHA_REPORTE---
"""
Primero se cambian los '/' por '-' ya que es el formato de fecha que se va a seguir.
Posteriormente se intercambian los números adecuadamente para que el primero sea menor a 32, el segundo 
menor a 13 y el último sea de 4 digitos.
"""
for index, row in df.iterrows():
    fecha = row["FECHA_REPORTE"].replace('/', '-').split('-')
    if int(fecha[0]) > 31:
        # En el primer puesto está el año
        aux = fecha[0]
        fecha[0] = fecha[-1]
        fecha[-1] = aux
    if int(fecha[1]) > 12:
        aux = fecha[0]
        fecha[0] = fecha[1]
        fecha[1] = aux
    to_print = ''
    for num in fecha:
        to_print += num + '-'
    df.loc[index, "FECHA_REPORTE"] = to_print[:-1]

for index, row in df.iterrows():
    fecha = row["FECHA_REPORTE"].split('-')

    if int(fecha[1]) > 12:
        print(row)

#%% ---Escribir todo---
df.to_csv("./datasets/IncidentesSeguridadLimpio.csv", index=False)
