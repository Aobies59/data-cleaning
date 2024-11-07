import pandas as pd
import datetime

def corregir_formato_fecha(df, columna):
    formatos = ['%Y/%m/%d', '%Y-%m-%d', '%m-%d-%Y', '%d-%m-%Y', '%Y/%m/%d', '%d/%m/%Y']
    def convertir_fecha(fecha):
        for formato in formatos:
            try:
                return pd.to_datetime(fecha, format=formato).strftime('%d-%m-%Y')
            except ValueError:
                continue
        return fecha
    df[columna] = df[columna].apply(convertir_fecha)
    return df

def limpiar_id(df, columna):
    df[columna] = df[columna].str.replace('-', '', regex=False) \
                             .str.replace(',00', '', regex=False) \
                             .str.replace(' MT', '', regex=False) \
                             .str.replace('MNT', '', regex=False) \
                             .str.replace("'", '', regex=False) \
                             .str.replace('"', '', regex=False)

    columna_actualizada = []

    for currArray in df[columna]:
        currArray = currArray[1:-1]  # quitar los corchetes
        values = currArray.split(",")
        values_actualizados = []
        for value in values:
            value = value.strip()
            indice_no_cero = 0
            for currLetra in value:
                if currLetra == "0":
                    indice_no_cero += 1
                else:
                    break
            value = value[indice_no_cero:]
            values_actualizados.append(value)
        columna_actualizada.append(values_actualizados)

    df[columna] = columna_actualizada
    return df

# Función para obtener información de usuarios en columna de `UsuarioID`
def obtener_info_usuarios(df, columna, ruta_usuarios_limpios):
    df_usuarios = pd.read_csv(ruta_usuarios_limpios)
    columna_actualizada = []
    for currArray in df[columna]:
        currArray = currArray[1:-1]  # quitar los corchetes
        values = currArray.split(",")
        values_actualizados = []
        for value in values:
            index = df_usuarios.index[df_usuarios['NIF'] == value.strip()[1:-1]].tolist()
            info = []
            if index:
                info.append(df_usuarios.at[index[0], 'NOMBRE'])
                info.append(df_usuarios.loc[index[0], 'EMAIL'])
                info.append("+" + str(df_usuarios.loc[index[0], 'TELEFONO']))
            values_actualizados.append(info)
        columna_actualizada.append(values_actualizados)
    df['UserInfo'] = columna_actualizada
    return df

# Función para calcular tiempo de resolución
def obtener_tiemporesolucion(df2, col_mantenimiento_id, df1, col_id, fecha_df2, fecha_df1):
    df1[col_id] = df1[col_id].astype(str)
    for index, row in df2.iterrows():
        temp = []
        for man_id in row[col_mantenimiento_id]:
            man_id = str(man_id).strip()
            if man_id in df1[col_id].values:
                fecha_intervencion = df1.loc[df1[col_id] == man_id, fecha_df1].values[0]
                fecha_reporte = row[fecha_df2]
                if pd.notnull(fecha_intervencion) and pd.notnull(fecha_reporte):
                    fecha_reporte = datetime.datetime.strptime(fecha_reporte, '%d-%m-%Y')
                    fecha_intervencion = datetime.datetime.strptime(fecha_intervencion, '%d-%m-%Y')
                    diferencia_dias = (fecha_intervencion - fecha_reporte).days
                    temp.append(max(diferencia_dias, -1))
        tiempo_resolucion = max(temp) if temp else -1
        df2.at[index, 'tiempoResolucion'] = tiempo_resolucion

    return df2

# Guardar CSV
def guardar_csv(df, ruta_guardado):
    try:
        df.to_csv(ruta_guardado, index=False)
        print(f"Archivo guardado en {ruta_guardado}.")
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")

# Procesar archivo de incidencias de usuarios
ruta_archivo = "datasets/IncidenciasUsuariosSucio.csv"
ruta_guardado = "datasets/IncidenciasUsuariosLimpio.csv"
ruta_usuarios_limpios = 'datasets/UsuariosLimpio.csv'
ruta_mantenimiento = 'datasets/MantenimientoLimpio.csv'

def main():
    df = pd.read_csv(ruta_archivo)
    df_mantenimiento = pd.read_csv(ruta_mantenimiento)

    if df is not None and df_mantenimiento is not None:
        df = corregir_formato_fecha(df, 'FECHA_REPORTE')
        df = limpiar_id(df, 'MantenimeintoID')
        df['nivelEscalamiento'] = 'Bajo'
        df = df.rename(columns={'MantenimeintoID': 'MantenimientoID'})

        # Obtener información de usuarios y tiempo de resolución
        df = obtener_info_usuarios(df, 'UsuarioID', ruta_usuarios_limpios)
        df = obtener_tiemporesolucion(df, 'MantenimientoID', df_mantenimiento, 'ID', 'FECHA_REPORTE', 'FECHA_INTERVENCION')

        guardar_csv(df, ruta_guardado)

if __name__ == "__main__":
    main()
