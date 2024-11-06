import pandas as pd



df = pd.read_csv("datasets/meteo24.csv", delimiter=';')

# Borramos las columnas PROVINCIA, MUNICIPIO y ESTACIÓN porque tenemos PUNTO_MUESTREO
df = df.drop(columns=['PROVINCIA', 'MUNICIPIO', 'ESTACION'])
df['PUNTO_MUESTREO'] = df['PUNTO_MUESTREO'].str.split('_').str[0].astype(int)


# Cambiar nombre columna ESTACIÓN
df = df.rename(columns={'ESTACION': 'ESTACIÓN'})


# Cambiar nombre de la columna AÑO
df = df.rename(columns={'ANO': 'AÑO'})


columnas_metadata = ['PUNTO_MUESTREO', 'MAGNITUD', 'AÑO', 'MES']
columnas_dias_d = [col for col in df.columns if col.startswith('D')]
columnas_dias_v = [col for col in df.columns if col.startswith('V')]

# Usar melt para apilar las columnas D y V
df_d = df.melt(id_vars=columnas_metadata, value_vars=columnas_dias_d, 
               var_name='DÍA', value_name='D')
df_v = df.melt(id_vars=columnas_metadata, value_vars=columnas_dias_v, 
               var_name='DÍA', value_name='V')

# Limpiar la columna DÍA
df_d['DÍA'] = df_d['DÍA'].str.extract('(\d+)').astype(int)
df_v['DÍA'] = df_v['DÍA'].str.extract('(\d+)').astype(int)

# Combinar los DataFrames en uno solo
df = pd.merge(df_d, df_v, on=columnas_metadata + ['DÍA'])

# Eliminar las filas que no sean válidas
df = df[df['V'] != 'N']


df = df[df["MAGNITUD"] != 82]
df = df[df["MAGNITUD"] != 86]
df = df[df["MAGNITUD"] != 87]
df = df[df["MAGNITUD"] != 88]




magnitudes = df["MAGNITUD"].unique()
magnitudes.sort()

# Inicializar las nuevas columnas
for magnitud in magnitudes:
    df[f'MAGNITUD_{magnitud}'] = None 

# Rellenar las nuevas columnas basadas en la columna MAGNITUD
for index, row in df.iterrows():
    if row['MAGNITUD'] in magnitudes:
        df.loc[index, f'MAGNITUD_{row["MAGNITUD"]}'] = row['D']

# Eliminar la columna original MAGNITUD
df = df.drop(columns=['MAGNITUD'])


# Cambiamos el nombre de cada columna por su correspondiente
df = df.rename(columns={'MAGNITUD_81': 'V_VIENTO'})
df = df.rename(columns={'MAGNITUD_83': 'TEMPERATURA'})
df = df.rename(columns={'MAGNITUD_89': 'PRECIPITACION'})

# Cómo ya están en otras columnas, quitamos la columna de medidas
df = df.drop(columns=["D"])


# Agrupamos para que en el mismo día y estación aparezcan las mediciones
df = df.groupby(['PUNTO_MUESTREO', 'AÑO', 'MES', 'DÍA', 'V']).agg({
    'V_VIENTO': 'first',
    'TEMPERATURA': 'first',
    'PRECIPITACION': 'first'
}).reset_index()


for valor in df['V_VIENTO']:
    if valor:
        if valor >= 11.39:
            print(valor)
df['V_VIENTO'] = df['V_VIENTO'] >= 11.39

# Cómo ni el viento ni la precipitación pueden ser negativos, ponemos -1 cómo nulo
df[['PRECIPITACION']] = df[['PRECIPITACION']].fillna(-1)
df[['TEMPERATURA']] = df[['TEMPERATURA']].fillna(100)


df = df.sort_values(by=["PUNTO_MUESTREO", "AÑO", "MES", "DÍA"])


df = df.rename(columns={'AÑO': 'year', 'MES': 'month', 'DÍA': 'day'})

# Crear la columna de fecha
df['FECHA'] = pd.to_datetime(df[['year', 'month', 'day']]).dt.strftime('%d-%m-%Y')

# Renombrar las columnas de vuelta a su nombre original
df = df.rename(columns={'year': 'AÑO', 'month': 'MES', 'day': 'DÍA'})

# Eliminar las columnas individuales si no se necesitan
df = df.drop(columns=['AÑO', 'MES', 'DÍA', 'V'])



# Reordenar el dataframe
df = df[['PUNTO_MUESTREO', 'FECHA', 'V_VIENTO', 'TEMPERATURA', 'PRECIPITACION']]


aux_df = pd.read_csv("datasets/estaciones_meteo_CodigoPostal.csv", sep=";")

aux_df = aux_df.rename(columns={'CÓDIGO': 'PUNTO_MUESTREO'})


df = df.merge(aux_df[['PUNTO_MUESTREO', 'Codigo Postal']], on='PUNTO_MUESTREO', how='left')

df['Codigo Postal'] = df['Codigo Postal'].str.replace(', ', '-')

df = df.rename(columns={'Codigo Postal': 'CODIGO_POSTAL'})

df = df[['PUNTO_MUESTREO', 'CODIGO_POSTAL', 'FECHA', 'V_VIENTO', 'TEMPERATURA', 'PRECIPITACION']]

df['CODIGO_POSTAL'] = df['CODIGO_POSTAL'].apply(lambda x: list(map(int, x.split('-'))))

df.index += 1

df.to_csv("./datasets/meteo_limpio.csv", index=True, index_label="ID")
