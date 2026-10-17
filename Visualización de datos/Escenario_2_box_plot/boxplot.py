
import json
import matplotlib.pyplot as plt
from pathlib import Path

#Leer el archivo JSON
ruta = Path(__file__).resolve().parent / "datos_salarios.json"

with open(ruta, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

#Obtener los departamentos del archivo
departamentos = sorted(set(registro["group"] for registro in datos))

#Agrupar los salarios por departamento
salarios = [
    [registro["score"] for registro in datos
     if registro["group"] == departamento]
    for departamento in departamentos
]


#Crear el box plot con el formato de referencia
plt.figure(figsize=(11, 6))

plt.boxplot(
    salarios,
    labels=departamentos,
    showmeans=False,
    patch_artist=False,
    medianprops=dict(color="#ff7f0e", linewidth=1),
    flierprops=dict(
        marker="o",
        markerfacecolor="white",
        markeredgecolor="black",
        markersize=5
    )
)

plt.title("Distribución de salarios por departamento")
plt.xlabel("Departamento")
plt.ylabel("Salario mensual (MXN)")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="-", alpha=0.3)
plt.tight_layout()
plt.show()
