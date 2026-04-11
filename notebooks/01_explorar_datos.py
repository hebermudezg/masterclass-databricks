# Databricks notebook source
# MAGIC %md
# MAGIC # ICFES Saber 11: Analitica de Datos Asistida por IA
# MAGIC
# MAGIC Exploramos resultados reales del examen Saber 11 para descubrir
# MAGIC que factores influyen en el rendimiento academico.
# MAGIC
# MAGIC - **Dataset:** 27,000+ resultados del Saber 11 (2022)
# MAGIC - **Fuente:** [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe)
# MAGIC - **Variables:** Estrato, tipo de colegio, educacion de los padres, acceso a internet, puntajes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Cargar datos

# COMMAND ----------

import pandas as pd
import numpy as np

URL = "https://raw.githubusercontent.com/hebermudezg/masterclass-databricks/main/dataset/icfes_saber11.csv"
df = pd.read_csv(URL)
print(f"Dataset: {df.shape[0]:,} estudiantes x {df.shape[1]} variables")

# COMMAND ----------

df.head()

# COMMAND ----------

df.describe()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Guardar como tabla Delta
# MAGIC
# MAGIC **Delta Lake** es el formato nativo de Databricks para almacenar datos.
# MAGIC Funciona como una tabla de base de datos optimizada para consultas rapidas
# MAGIC sobre grandes volumenes, con versionado automatico incluido.
# MAGIC
# MAGIC Al guardar como tabla Delta, herramientas como **Genie** y el **Editor SQL**
# MAGIC pueden acceder a los datos directamente.

# COMMAND ----------

spark_df = spark.createDataFrame(df)
spark_df.write.mode("overwrite").saveAsTable("default.icfes_saber11")
print(f"Tabla Delta creada: default.icfes_saber11 ({len(df):,} filas)")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) as total_estudiantes,
# MAGIC        ROUND(AVG(punt_global), 0) as puntaje_promedio,
# MAGIC        ROUND(MIN(punt_global), 0) as minimo,
# MAGIC        ROUND(MAX(punt_global), 0) as maximo
# MAGIC FROM default.icfes_saber11

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Explorar con Genie
# MAGIC
# MAGIC Genie es el asistente de IA de Databricks. Permite consultar tablas
# MAGIC usando lenguaje natural: escribes una pregunta y Genie genera el SQL,
# MAGIC ejecuta la consulta y muestra el resultado.
# MAGIC
# MAGIC **Como usarlo:** Menu lateral > **Genie** > seleccionar `default.icfes_saber11`
# MAGIC
# MAGIC Ejemplos de preguntas:
# MAGIC - Cual es el puntaje promedio por estrato?
# MAGIC - Hay diferencia entre colegios oficiales y privados?
# MAGIC - Los estudiantes con internet tienen mejor puntaje?
# MAGIC - Cuales son los mejores departamentos?
# MAGIC - Que porcentaje de estrato 1 supera los 300 puntos?

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Visualizaciones

# COMMAND ----------

import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

# Distribucion del puntaje global
fig, ax = plt.subplots(figsize=(12, 5))
df["punt_global"].hist(bins=60, ax=ax, color="#1565C0", edgecolor="white", alpha=0.85)
media = df["punt_global"].mean()
mediana = df["punt_global"].median()
ax.axvline(media, color="red", linestyle="--", linewidth=2, label=f"Promedio: {media:.0f}")
ax.axvline(mediana, color="orange", linestyle="--", linewidth=2, label=f"Mediana: {mediana:.0f}")
ax.set_title("Distribucion del Puntaje Global - ICFES Saber 11", fontsize=15, fontweight="bold")
ax.set_xlabel("Puntaje Global")
ax.set_ylabel("Frecuencia")
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Puntaje promedio por estrato
fig, ax = plt.subplots(figsize=(12, 6))
orden_estrato = ["Estrato 1", "Estrato 2", "Estrato 3", "Estrato 4", "Estrato 5", "Estrato 6"]
estrato_stats = (
    df[df["fami_estratovivienda"].isin(orden_estrato)]
    .groupby("fami_estratovivienda")["punt_global"]
    .agg(["mean", "count"])
)
estrato_stats = estrato_stats.reindex(orden_estrato)
colores = plt.cm.RdYlGn(np.linspace(0.15, 0.95, len(estrato_stats)))
ax.bar(range(len(estrato_stats)), estrato_stats["mean"], color=colores, edgecolor="white", width=0.7)
ax.set_xticks(range(len(estrato_stats)))
ax.set_xticklabels(orden_estrato, fontsize=12)
for i, (idx, row) in enumerate(estrato_stats.iterrows()):
    ax.text(i, row["mean"] + 1, f'{row["mean"]:.0f}', ha="center", fontweight="bold", fontsize=13)
    ax.text(i, row["mean"] - 8, f'n={row["count"]:,.0f}', ha="center", fontsize=9, color="white")
ax.set_title("Puntaje Promedio por Estrato Socioeconomico", fontsize=15, fontweight="bold")
ax.set_ylabel("Puntaje Promedio", fontsize=12)
ax.set_ylim(0, estrato_stats["mean"].max() * 1.15)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Comparaciones clave
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Oficial vs Privado
ax = axes[0, 0]
tipo = df.groupby("cole_naturaleza")["punt_global"].mean().sort_values()
tipo.plot(kind="barh", ax=ax, color=["#E53935", "#43A047"], edgecolor="white")
for i, (idx, val) in enumerate(tipo.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Colegio Oficial vs Privado", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# Urbano vs Rural
ax = axes[0, 1]
area = df.groupby("cole_area_ubicacion")["punt_global"].mean().sort_values()
area.plot(kind="barh", ax=ax, color=["#FF8F00", "#1565C0"], edgecolor="white")
for i, (idx, val) in enumerate(area.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Urbano vs Rural", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# Internet
ax = axes[1, 0]
internet = df.groupby("fami_tieneinternet")["punt_global"].mean().sort_values()
internet.plot(kind="barh", ax=ax, color=["#E53935", "#43A047"], edgecolor="white")
for i, (idx, val) in enumerate(internet.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Tiene Internet en Casa?", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# Genero
ax = axes[1, 1]
genero = df.groupby("estu_genero")["punt_global"].mean().sort_values()
genero_labels = genero.rename(index={"F": "Femenino", "M": "Masculino"})
genero_labels.plot(kind="barh", ax=ax, color=["#E91E63", "#1565C0"], edgecolor="white")
for i, (idx, val) in enumerate(genero_labels.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Genero", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

plt.suptitle("Factores que impactan el puntaje del ICFES", fontsize=17, fontweight="bold", y=1.02)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Educacion de la madre vs puntaje
fig, ax = plt.subplots(figsize=(14, 7))
orden_edu = [
    "Ninguno", "Primaria incompleta", "Primaria completa",
    "Secundaria (Bachillerato) incompleta", "Secundaria (Bachillerato) completa",
    u"T\u00e9cnica o tecnol\u00f3gica incompleta", u"T\u00e9cnica o tecnol\u00f3gica completa",
    u"Educaci\u00f3n profesional incompleta", u"Educaci\u00f3n profesional completa",
    "Postgrado",
]
edu_madre = df.groupby("fami_educacionmadre")["punt_global"].mean()
edu_madre = edu_madre.reindex([x for x in orden_edu if x in edu_madre.index])
colores = plt.cm.viridis(np.linspace(0.15, 0.95, len(edu_madre)))
ax.barh(range(len(edu_madre)), edu_madre.values, color=colores, edgecolor="white")
ax.set_yticks(range(len(edu_madre)))
ax.set_yticklabels(edu_madre.index, fontsize=11)
for i, val in enumerate(edu_madre.values):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold")
ax.set_title("Puntaje Promedio segun Educacion de la Madre", fontsize=15, fontweight="bold")
ax.set_xlabel("Puntaje Promedio", fontsize=12)
plt.tight_layout()
plt.show()

# COMMAND ----------

# Ranking de departamentos
fig, ax = plt.subplots(figsize=(14, 8))
depto = (
    df.groupby("cole_depto_ubicacion")["punt_global"]
    .agg(["mean", "count"])
    .query("count >= 50")
    .sort_values("mean")
)
n = len(depto)
colores = ["#E53935"] * min(5, n) + ["#9E9E9E"] * max(0, n - 10) + ["#43A047"] * min(5, n)
ax.barh(range(n), depto["mean"], color=colores[:n], edgecolor="white")
ax.set_yticks(range(n))
ax.set_yticklabels(depto.index, fontsize=10)
ax.set_title("Puntaje Promedio por Departamento", fontsize=15, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")
plt.tight_layout()
plt.show()
