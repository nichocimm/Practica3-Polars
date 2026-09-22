import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

def eda_geografico(df):
    df_limpio = df.with_columns(
        pl.col("nom_entidad")
        .str.replace_all(r"[^\x00-\x7F]", "") 
        .str.strip_chars()
    )

    prevalencia_estado = (
        df_limpio.group_by("nom_entidad")
        .agg([
            pl.col("sufrio_violencia_pareja").mean().alias("porcentaje_violencia")
        ])
        .sort("porcentaje_violencia", descending=True)
        .to_pandas()
    )
    prevalencia_estado["porcentaje_violencia"] *= 100
    plt.rcParams['font.family'] = 'sans-serif'

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=prevalencia_estado,
        x="porcentaje_violencia",
        y="nom_entidad",
        hue="nom_entidad",   
        legend=False,           
        palette="flare"
    )
    
    plt.title("Prevalencia de Violencia de Pareja por Entidad Federativa (%)")
    plt.xlabel("Porcentaje de Mujeres que Reportaron Violencia")
    plt.ylabel("Estado")
    plt.tight_layout()
    plt.show()