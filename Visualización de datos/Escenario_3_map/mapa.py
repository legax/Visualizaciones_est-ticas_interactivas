
import json
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

#Leer el JSON
carpeta = Path(__file__).resolve().parent

with open(carpeta / "datos_municipios.json",
          "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

df = pd.DataFrame(datos)

#Cargar los límites geográficos de Aguascalientes
url = "https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/01"
mapa = gpd.read_file(url)

#Identificar la columna con los nombres municipales
col_nombre = next(
    (c for c in ["nomgeo", "nom_mun", "NOMGEO", "nombre"]
     if c in mapa.columns),
    None
)

if col_nombre is None:
    raise ValueError("No se encontró la columna de nombres municipales.")

#Unir los datos del JSON con el mapa
mapa["municipio"] = mapa[col_nombre].astype(str).str.strip()

df["category"] = df["category"].astype(str).str.strip()

mapa = mapa.merge(
    df,
    left_on="municipio",
    right_on="category",
    how="left"
)


#Crear el mapa coroplético
fig, ax = plt.subplots(figsize=(12, 10))

mapa.plot(
    column="value",
    cmap="OrRd",
    linewidth=0.8,
    edgecolor="black",
    legend=True,
    missing_kwds={
        "color": "lightgrey",
        "label": "Sin datos"
    },
    legend_kwds={"label": "Casos confirmados"},
    ax=ax
)

#Agregar etiquetas de los municipios
mapa_proyectado = mapa.to_crs(epsg=6372)
puntos = mapa_proyectado.geometry.representative_point().to_crs(mapa.crs)

for i, punto in enumerate(puntos):
    nombre = mapa.iloc[i]["municipio"]

    ax.annotate(
        nombre,
        xy=(punto.x, punto.y),
        ha="center",
        va="center",
        fontsize=7,
        color="black",
        fontweight="bold"
    )

ax.set_title("Casos confirmados por municipio", fontsize=14)
ax.set_axis_off()

plt.tight_layout()
plt.show()
