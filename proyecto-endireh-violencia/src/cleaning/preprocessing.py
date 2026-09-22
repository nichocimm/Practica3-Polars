import polars as pl
from config.rutas import RUTA_DATA_RAW, RUTA_DATA_PROCESSED

# Lee el archivo "endireh_ml_dataset.csv" y devuelve el DataFrame
def leer():
    return pl.read_csv(RUTA_DATA_RAW / "endireh_ml_dataset.csv")

# Te da el valor del porcentaje del 0 al 100 de los valores nulos 
def detectar_porcentaje_de_nulos(df, col):
    rows = len(df)
    nulls = df[col].null_count()
    return nulls * 100 / rows

# Quita nulos de la siguiente manera
#  + Si tiene menos del 3% de nulos, borra las filas que contengan 
#  + Si tiene de 3% hasta 60% simplemente imputa los datos de la mediana o con "N/A"
#  + Si tiene más del 60% entonces borra la columna completa por falta de datos
#  + Si las columnas revisadas vienen con nulo, por otras cuestiones se le imputa un valor
#    adecuado
def quitar_nulos(df):
    imputar_col = []
    eliminar_row_col = []
    columnas_revisadas_por_imputar = ["ingreso_pareja","num_hijos"]
    for col in df.columns: 
        porcentaje = detectar_porcentaje_de_nulos(df,col)
        if porcentaje == 0:
            continue
        if(col in columnas_revisadas_por_imputar):
            imputar_col.append(pl.col(col).fill_null(0))
            continue
        if porcentaje <= 3:
            eliminar_row_col.append(col)
        else:
            if df[col].dtype.is_numeric():
                mediana = df[col].median()
                imputar_col.append(pl.col(col).fill_null(mediana))
            else:
                imputar_col.append(pl.col(col).fill_null("N/A"))
    df_limpio = (df.lazy().drop_nulls(eliminar_row_col))
    if imputar_col:
        df_limpio = df_limpio.with_columns(imputar_col)
    datos_sin_nulos = df_limpio.collect()
    columnas_repetidas = [
        col for col in datos_sin_nulos.columns 
        if df[col].n_unique() == 1
    ]
    return datos_sin_nulos.drop(columnas_repetidas)

# Normaliza las expresiones
def normalizar(df):
    col_final = []
    columnas_revisadas = ["nivel_escolaridad"]
    for col in df.columns:
        if df[col].dtype.is_numeric() or col in columnas_revisadas:
            if df[col].dtype in [pl.Float32, pl.Float64]:
                col_final.append(df[col].cast(pl.Int32))
            else:
                col_final.append(df[col])
            continue
        if df[col].dtype == pl.String:
            nulos_orig = df[col].null_count()
            limpio = (
                df[col]
                .str.strip_chars()
                .str.extract(r"(\d+)")
                .cast(pl.Int32, strict=False)
            )
            nulos_desp = limpio.null_count()

            if nulos_desp > nulos_orig:
                col_final.append(df[col].str.to_lowercase().str.strip_chars())
            else:
                col_final.append(limpio)
    return pl.DataFrame(col_final)

# Crea las variables nuevas, para su posterior análisis
# + autonomia_financiera - sirve para ver el nivel de autonomia financiera
# + bloque_educativo     - sirve para ver en que nivel educativo se encuentran
def crear_nuevas_variables(df):
    df_nuevas_variables = df.with_columns([

        pl.when((pl.col("dinero_propio_id") == 1) & (pl.col("tiene_ahorros_id") == 1))
        .then(pl.lit("alta"))
        .when((pl.col("dinero_propio_id") == 1) | (pl.col("tiene_ahorros_id") == 1))
        .then(pl.lit("media"))
        .otherwise(pl.lit("baja"))
        .alias("autonomia_financiera"),

        pl.when(pl.col("nivel_escolaridad").str.starts_with("A"))
        .then(pl.lit("basica_o_primaria"))
        .when(pl.col("nivel_escolaridad").str.starts_with("B"))
        .then(pl.lit("secundaria_o_bachillerato"))
        .when(pl.col("nivel_escolaridad").str.starts_with("C"))
        .then(pl.lit("superior_o_posgrado"))
        .otherwise(pl.lit("otro_o_no_especificado"))
        .alias("bloque_educativo")
    ])

    return df_nuevas_variables

# Escribe el DataFrame resultante en los datos procesados.
# Devuelve el mismo DataFrame para poder consultarlo desde codigo.
def escribir(df):
    df.write_csv(str(RUTA_DATA_PROCESSED / "endireh_datos_procesados.csv"))
    return df

# Ejecuta todo el pipeline del preprocesamiento del archivo.
# Devuelve un DataFrame con los datos limpios.
def pipeline_preprocesamiento():
    df_crudo = leer()
    df_normalizado = normalizar(df_crudo)
    df_sin_nulos = quitar_nulos(df_normalizado)
    df_procesado = crear_nuevas_variables(df_sin_nulos)
    return escribir(df_procesado)

pipeline_preprocesamiento()