import pandas as pd

# Función para corregir formato de fecha
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

# Función para limpiar IDs
def limpiar_id(df, columna):
    df[columna] = df[columna].str.replace('-', '', regex=False) \
                             .str.replace(',00', '', regex=False) \
                             .str.replace(' MT', '', regex=False) \
                             .str.replace('MNT', '', regex=False) \
                             .str.replace("'", '', regex=False) \
                             .str.replace('"', '', regex=False)
    return df

# Guardar CSV
def guardar_csv(df, ruta_guardado):
    try:
        df.to_csv(ruta_guardado, index=False)
        print(f"Archivo guardado en {ruta_guardado}.")
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")

# Definir rutas de archivos
ruta_archivo = "datasets/MantenimientoSucio.csv"
ruta_guardado = "datasets/MantenimientoLimpio.csv"



def main():
    # Procesar archivo de mantenimiento
    df = pd.read_csv(ruta_archivo)
    if df is not None:
        df = corregir_formato_fecha(df, 'FECHA_INTERVENCION')
        df = limpiar_id(df, 'ID')
        df['ID'] = df['ID'].astype(str).str.strip()
        df = df.drop(columns=['Tipo'])
        guardar_csv(df, ruta_guardado)




if __name__ == "__main__":
    main()
