import pandas as pd
from random import randint 

df_areas = pd.read_csv("datasets/AreasSucio.csv")
df_incidentes = pd.read_csv("datasets/IncidentesSeguridadLimpio.csv")
df_encuestas = pd.read_csv("datasets/EncuestasSatisfaccionLimpio.csv")
df_juegos = pd.read_csv("datasets/JuegosLimpio.csv")
df_meteo = pd.read_csv("datasets/meteo_limpio.csv")
print(df_incidentes["GRAVEDAD"].unique())
#%% ---LIMPIEZA FECHA_INSTALACION---
"""
Las fechas vienen en varios formatos diferentes, por lo que se va a emplear
en todos ellos el formato dd-mm-yyyy. Para esto, se consideran los siguientes
aspectos para cada uno de los formatos:
    - La hora de algunos formatos no es interesante, se borra.
    - Las fechas cuyo formato sea dd-mm-yy se añade 20 o 19 al principio del 
      último parámetro.
    - Se cambian los números para que la fecha sea coherente, es decir, el
      primer valor menor a 32, el segundo menor a 13 y el último mayor de 100.
    - Para las fechas que no están definidas se va a poner por deecto la fecha
      más antigua que exista en la columna (01-01-1996).
"""
def maximo_lista(lista: list):
    max_num = -100
    for num in lista:
        max_num = max(int(num), max_num)
    return max_num
years = []
for index, row in df_areas.iterrows():
    if type(row["FECHA_INSTALACION"]) == float or row["FECHA_INSTALACION"] == "fecha_incorrecta":
        df_areas.loc[index, "FECHA_INSTALACION"] = "01-01-1996"
    else:
        if len(row["FECHA_INSTALACION"]) > 10:
            df_areas.loc[index, "FECHA_INSTALACION"] = df_areas.loc[index, "FECHA_INSTALACION"][:-9]
            row["FECHA_INSTALACION"] = df_areas.loc[index, "FECHA_INSTALACION"][:-9]
        df_areas.loc[index, "FECHA_INSTALACION"] = df_areas.loc[index, "FECHA_INSTALACION"].replace('/', '-')
        fecha = df_areas.loc[index, "FECHA_INSTALACION"].split('-')
        a = maximo_lista(fecha)
        if a < 100 and int(fecha[-1]) < 25:
            fecha[-1] = str(int(fecha[-1]) + 2000)
        elif a < 100:
            fecha[-1] = str(int(fecha[-1]) + 1900)
        if int(fecha[0]) > 31:
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
        df_areas.loc[index, "FECHA_INSTALACION"] = to_print[:-1]
df_areas = df_areas.rename(columns={"FECHA_INSTALACION": "fechaInstalacion"})

#%% ---LIMPIEZA COORDENADAS---
"""
No nos interesa el sistema de coordenadas que se utiliza, puesto que es siempre el mismo,
por lo que esta columna puede borrarse.

Para agrupar los dos valores en unna única columna, podemos generar tuplas cuyo primer
valor sea la latitud y las segunda la longitud, por lo que es lo que se va a hacer,
manteniendo todos los decimales de las dos coordenadas.

Seha decidido usar el sistema de coordenadas global, debido a que es más preciso que el
europeo utilizando las otras dos coordenadas del dataframe.
"""

df_areas['coordenadasGPS'] = df_areas.apply(lambda row: (row['LONGITUD'], row['LATITUD']), axis=1)

df_areas = df_areas.drop(columns=["SISTEMA_COORD", "LATITUD", "LONGITUD"])

#%% ---LIMPIEZA BARRIO---
"""
Se tienen que quitar los caracteres con acentos y se van a poner en mayusculas todas las
letras después de espacio y la primera letra del barrio.
"""
for index, row in df_areas.iterrows():
    barrio = row["BARRIO"].lower()    
    for i in range(len(barrio)):
        if barrio[i] == "á":
            if i != len(barrio) - 1:
                barrio = barrio[:i] + "a" + barrio[i + 1:]
            else:
                barrio = barrio[:i] + "a"
        elif barrio[i] == "é":
            if i != len(barrio) - 1:
                barrio = barrio[:i] + "e" + barrio[i + 1:]
            else:
                barrio = barrio[:i] + "e"
        elif barrio[i] == "í":
            if i != len(barrio) - 1:
                barrio = barrio[:i] + "i" + barrio[i + 1:]
            else:
                barrio = barrio[:i] + "i"
        elif barrio[i] == "ó":
            if i != len(barrio) - 1:
                barrio = barrio[:i] + "o" + barrio[i + 1:]
            else:
                barrio = barrio[:i] + "o"
        elif barrio[i] == "ú":
            if i != len(barrio) - 1:
                barrio = barrio[:i] + "u" + barrio[i + 1:]
            else:
                barrio = barrio[:i] + "u"
        if barrio[i-1] == " ":
            barrio = barrio[:i] + barrio[i].upper() + barrio[i + 1:]
    barrio = barrio[0].upper() + barrio[1:]
    df_areas.loc[index, "BARRIO"] = barrio
df_areas = df_areas.rename(columns={"BARRIO": "barrio"})

#%% ---LIMPIEZA DISTRITO---
"""
Debe hacerse la misma limpieza que para barrio, pero teniendo en cuenta que puede haber
valores nulos. A los valores nulos se les va a poner como valor por defecto 
'ID-distrito-ausente'
"""
for index, row in df_areas.iterrows():
    if type(row["DISTRITO"]) == float:
        barrio = str(row["ID"]) + "-distrito-ausente"
    else:
        barrio = row["DISTRITO"].lower()
        for i in range(len(barrio)):
            if barrio[i] == "á":
                if i != len(barrio) - 1:
                    barrio = barrio[:i] + "a" + barrio[i + 1:]
                else:
                    barrio = barrio[:i] + "a"
            elif barrio[i] == "é":
                if i != len(barrio) - 1:
                    barrio = barrio[:i] + "e" + barrio[i + 1:]
                else:
                    barrio = barrio[:i] + "e"
            elif barrio[i] == "í":
                if i != len(barrio) - 1:
                    barrio = barrio[:i] + "i" + barrio[i + 1:]
                else:
                    barrio = barrio[:i] + "i"
            elif barrio[i] == "ó":
                if i != len(barrio) - 1:
                    barrio = barrio[:i] + "o" + barrio[i + 1:]
                else:
                    barrio = barrio[:i] + "o"
            elif barrio[i] == "ú":
                if i != len(barrio) - 1:
                    barrio = barrio[:i] + "u" + barrio[i + 1:]
                else:
                    barrio = barrio[:i] + "u"
            if barrio[i-1] == " ":
                barrio = barrio[:i] + barrio[i].upper() + barrio[i + 1:]
        barrio = barrio[0].upper() + barrio[1:]
    df_areas.loc[index, "DISTRITO"] = barrio
df_areas = df_areas.rename(columns={"DISTRITO": "distrito"})

#%% ---LIMPIEZA ESTADO---
"""
Todas las áreas están en estado operativo, por lo que se ha decidido que su valor en la 
enumeracion sea 0, el resto de estados se añadiran mas tarde con numeros diferentes.
"""
for index, row in df_areas.iterrows():
    df_areas.loc[index, "ESTADO"] = "OPERATIVO"
df_areas = df_areas.rename(columns={"ESTADO": "estadoOperativo"})



#%% ---LIMPIEZA nombre---
"""
Para esto hemos decidido que el nombre del area sea el id concatenado con el
barrio y el nombre del barrio separado por '-' en el caso de que haya espacios
"""
df_areas["nombre"] = "AREA-" + df_areas["ID"].astype(str)

#%% ---RESUMEN Incidentes---
"""
Para esto vamos a crear diccionarios con la fecha, el tipo y la gravedad de los
incidentes de seguridad, añadiendolos a una lista por si existen varias referencias
al mismo ID del area recreativa
"""
incidentes_agrupados = (
    df_incidentes.groupby('AreaRecreativaID')
    .agg(
        incidentes=('FECHA_REPORTE', lambda x: [
            [   
                id,
                fecha,
                tipo,
                gravedad
            ]
            for id, fecha, tipo, gravedad in zip(df_incidentes.loc[x.index, 'ID'], x, df_incidentes.loc[x.index, 'TIPO_INCIDENTE'], df_incidentes.loc[x.index, 'GRAVEDAD'])
        ])
    )
)

incidentes_agrupados_dict = incidentes_agrupados['incidentes'].to_dict()

df_areas['incidentesSeguridad'] = df_areas['ID'].map(incidentes_agrupados_dict)

df_areas['incidentesSeguridad'] = df_areas['incidentesSeguridad'].apply(lambda x: x if isinstance(x, list) else [])

#%% ---RESUMEN Encuestas---
"""
Se deben agrupar las encuestas de satisfaccion por cada AreaRecreativaID y luego
asignarlo en una nueva columna del dataset.
"""

encuestas_agrupadas = df_encuestas.groupby("AreaRecreativaID")["ID"].apply(list).to_dict()

df_areas["encuestasSatisfaccion"] = df_areas["ID"].map(encuestas_agrupadas)

df_areas["encuestasSatisfaccion"] = df_areas["encuestasSatisfaccion"].apply(lambda x: x if isinstance(x, list) else [])

#%% ---RESUMEN Meteo---
"""
Estas dos tablas se relacionan por los codigos postales.
Para esto, vamos a generar una columna que tenga una lista con los ID de los sucesos
meteorológicos que afectan a dicho area.

""" 
codigos_meteo = {}
for index, row in df_meteo.iterrows():
    for codigo in row["CODIGO_POSTAL"].strip("[]").split(","):
        if codigo.strip() not in codigos_meteo.keys():
            codigos_meteo[codigo.strip()] = [row["ID"]]
        else:
            codigos_meteo[codigo.strip()].append(row["ID"])

df_areas["RegistroClima"] = [[] for _ in range(len(df_areas))]

for index, row in df_areas.iterrows():
    try:
        if str(int(row["COD_POSTAL"])) in codigos_meteo.keys():
            for id in codigos_meteo[str(int(row["COD_POSTAL"]))]:
                if id not in df_areas.loc[index, "RegistroClima"]:
                    df_areas.loc[index, "RegistroClima"].append(id)
    except:
        pass

#%% ---REFERENCIA Juegos---
"""
Tenemos que agrupar los juegos con los ID de las areas, por lo que primero
agrupamos estos valores y luego los asignamos a cada area respectivamente.
"""

juegos_agrupados = (
    df_juegos.groupby("AreaID")["ID"]
    .apply(list)
    .to_dict()
)

df_areas["Juego"] = df_areas["ID"].map(juegos_agrupados).apply(lambda x: x if isinstance(x, list) else [])

#%% ---LIMPIEZA capacidadMAX---
"""
Para este valor se va a tener en cuenta la capacidad máxima de cada zona.
La capacidad de cada area va a ser un numero aleatorio entre el doble del total de
juegos y el cuadruple de este mismo valor.
En el caso de que sea 0 el numero de juegos sera un numero aleatorio entre 2 y 4.
"""

df_areas["capacidadMAX"] = df_areas["Juego"].apply(lambda x: randint((len(x) + 1) * 2, (len(x) + 1) * 4))

#%% ---CREACION cantidadJuegosPorTipo---
"""
Para este valor vamos a crear una lista que en primera posicion tenga el numero de
juegos de tipo DEPORTIVAS, en segundo lugar INFANTIL y por ultimo MAYORES.
"""
df_areas["cantidadJuegosPorTipo"] = [[0, 0, 0] for _ in range(len(df_areas))]

for index, row in df_areas.iterrows():
    juegos = df_juegos.loc[df_juegos["AreaID"] == row["ID"], "TIPO"]
    for juego in juegos:
        if juego == "DEPORTIVO":
            df_areas.loc[index, "cantidadJuegosPorTipo"][0] += 1
        elif juego == "INFANTIL":
            df_areas.loc[index, "cantidadJuegosPorTipo"][1] += 1
        elif juego== "MAYORES":
            df_areas.loc[index, "cantidadJuegosPorTipo"][2] += 1


#%% Escritura de todo
df_areas = df_areas.drop(columns=["ID","DESC_CLASIFICACION","COD_BARRIO","COD_DISTRITO","COORD_GIS_X","COORD_GIS_Y","TIPO_VIA","NOM_VIA","NUM_VIA","COD_POSTAL","DIRECCION_AUX","NDP","CODIGO_INTERNO","CONTRATO_COD","TOTAL_ELEM","tipo"])
df_areas = df_areas[["nombre","estadoOperativo","fechaInstalacion","coordenadasGPS","capacidadMAX","barrio","distrito","incidentesSeguridad","encuestasSatisfaccion","RegistroClima","Juego","cantidadJuegosPorTipo"]]
df_areas.to_csv("datasets/AreasLimpio.csv", index=False)
