
import json
import matplotlib.pyplot as plt
from pathlib import Path

#Leer el archivo JSON
ruta = Path(__file__).resolve().parent / "datos_ventas.json"
with open(ruta, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

#Leer los trimestres directamente del archivo
trimestres = sorted(
    set(d["trimestre"] for d in datos),
    key=lambda t: (int(t.split("-T")[0]), int(t.split("-T")[1]))
)

#Obtener las categorías del archivo
categorias = sorted(set(d["categoria"] for d in datos))

#Crear la gráfica
plt.figure(figsize=(11, 6))

for categoria in categorias:
    registros = [
        d for d in datos if d["categoria"] == categoria
    ]
    
    registros.sort(key=lambda d: trimestres.index(d["trimestre"]))

    ventas = [d["ventas_miles_mxn"] for d in registros]
    periodos = [d["trimestre"] for d in registros]

    plt.plot(
        periodos,
        ventas,
        marker="o",
        linewidth=2,
        label=categoria
    )

plt.title("Evolución trimestral de ventas por categoría")
plt.xlabel("Trimestre")
plt.ylabel("Ventas (miles de MXN)")
plt.xticks(rotation=45)
plt.legend(title="Categoría")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()
