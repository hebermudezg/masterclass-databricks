# Databricks notebook source
# MAGIC %md
# MAGIC # Exploracion de Datos: ICFES Saber 11
# MAGIC
# MAGIC **Pregunta central:** Puede la IA predecir tu puntaje del ICFES solo con saber
# MAGIC tu estrato, tipo de colegio y si tienes internet en casa?
# MAGIC
# MAGIC **Dataset:** 7+ millones de resultados reales del Saber 11
# MAGIC **Fuente:** [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe)
# MAGIC
# MAGIC En este notebook:
# MAGIC 1. Cargamos datos reales del ICFES
# MAGIC 2. Limpiamos y preparamos
# MAGIC 3. Exploramos que factores impactan el rendimiento academico
# MAGIC 4. Guardamos datos limpios para el modelo de ML

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Cargar datos desde datos.gov.co

# COMMAND ----------

import pandas as pd
import numpy as np

# Descargamos 50,000 resultados recientes (periodos 2020+) con puntaje valido
# Para el dataset completo (7M filas), sube el CSV a un Volume y usa la linea comentada
URL_DATOS = (
    "https://www.datos.gov.co/resource/kgxf-xxbe.csv"
    "?$limit=50000"
    "&$where=punt_global%20IS%20NOT%20NULL%20AND%20periodo%20%3E%3D%20%2720201%27"
    "&$order=periodo%20DESC"
)

# Alternativa: cargar desde Volume (mas rapido si pre-subiste el CSV)
# URL_DATOS = "/Volumes/main/default/raw_data/icfes_saber11.csv"

print("Descargando resultados del ICFES Saber 11...")
df = pd.read_csv(URL_DATOS)
print(f"Dataset cargado: {df.shape[0]:,} filas x {df.shape[1]} columnas")

# COMMAND ----------

df.head()

# COMMAND ----------

# Las columnas se organizan en 4 grupos
grupos = {
    "Colegio (cole_)": [c for c in df.columns if c.startswith("cole_")],
    "Estudiante (estu_)": [c for c in df.columns if c.startswith("estu_")],
    "Familia (fami_)": [c for c in df.columns if c.startswith("fami_")],
    "Puntajes (punt_/desemp_)": [c for c in df.columns if c.startswith("punt_") or c.startswith("desemp_")],
}
for grupo, cols in grupos.items():
    print(f"\n{grupo}: {len(cols)} columnas")
    for col in cols:
        print(f"  - {col}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Limpieza de datos

# COMMAND ----------

# Eliminar duplicados (el dataset tiene filas repetidas)
antes = len(df)
df = df.drop_duplicates(subset=["estu_consecutivo"], keep="first")
print(f"Duplicados eliminados: {antes - len(df):,} filas")
print(f"Registros unicos: {len(df):,}")

# Convertir puntajes de texto a numerico
cols_puntaje = ["punt_global", "punt_matematicas", "punt_lectura_critica",
                "punt_c_naturales", "punt_sociales_ciudadanas", "punt_ingles"]
for col in cols_puntaje:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Filtrar registros con puntaje valido
df = df.dropna(subset=["punt_global"])

print(f"\nEstadisticas del puntaje global:")
print(f"  Promedio: {df['punt_global'].mean():.0f}")
print(f"  Mediana:  {df['punt_global'].median():.0f}")
print(f"  Min: {df['punt_global'].min():.0f} | Max: {df['punt_global'].max():.0f}")
print(f"  Desv. estandar: {df['punt_global'].std():.0f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Visualizaciones
# MAGIC
# MAGIC Vamos a responder visualmente:
# MAGIC - Importa el estrato socioeconomico?
# MAGIC - Colegio oficial vs privado: hay diferencia?
# MAGIC - Tener internet en casa cambia algo?
# MAGIC - Que tanto pesa la educacion de la mama?

# COMMAND ----------

import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")

# --- Distribucion del puntaje global ---
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

# --- EL GRAFICO CLAVE: Puntaje por estrato ---
fig, ax = plt.subplots(figsize=(12, 6))
orden_estrato = ["Estrato 1", "Estrato 2", "Estrato 3", "Estrato 4", "Estrato 5", "Estrato 6"]
estrato_stats = (
    df[df["fami_estratovivienda"].isin(orden_estrato)]
    .groupby("fami_estratovivienda")["punt_global"]
    .agg(["mean", "count"])
)
estrato_stats = estrato_stats.reindex(orden_estrato)
colores = plt.cm.RdYlGn(np.linspace(0.15, 0.95, len(estrato_stats)))
bars = ax.bar(range(len(estrato_stats)), estrato_stats["mean"], color=colores, edgecolor="white", width=0.7)
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

# --- Comparaciones clave: 4 paneles ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Oficial vs No Oficial
ax = axes[0, 0]
tipo = df.groupby("cole_naturaleza")["punt_global"].mean().sort_values()
tipo.plot(kind="barh", ax=ax, color=["#E53935", "#43A047"], edgecolor="white")
for i, (idx, val) in enumerate(tipo.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Colegio Oficial vs Privado", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# 2. Urbano vs Rural
ax = axes[0, 1]
area = df.groupby("cole_area_ubicacion")["punt_global"].mean().sort_values()
area.plot(kind="barh", ax=ax, color=["#FF8F00", "#1565C0"], edgecolor="white")
for i, (idx, val) in enumerate(area.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Urbano vs Rural", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# 3. Internet Si vs No
ax = axes[1, 0]
internet = df.groupby("fami_tieneinternet")["punt_global"].mean().sort_values()
internet.plot(kind="barh", ax=ax, color=["#E53935", "#43A047"], edgecolor="white")
for i, (idx, val) in enumerate(internet.items()):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold", fontsize=13)
ax.set_title("Tiene Internet en Casa?", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")

# 4. Genero
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

# --- Educacion de la madre vs puntaje ---
fig, ax = plt.subplots(figsize=(14, 7))
orden_edu = [
    "Ninguno", "Primaria incompleta", "Primaria completa",
    "Secundaria (Bachillerato) incompleta", "Secundaria (Bachillerato) completa",
    "Técnica o tecnológica incompleta", "Técnica o tecnológica completa",
    "Educación profesional incompleta", "Educación profesional completa",
    "Postgrado",
]
edu_madre = df.groupby("fami_educacionmadre")["punt_global"].mean()
edu_madre = edu_madre.reindex([x for x in orden_edu if x in edu_madre.index])
colores = plt.cm.viridis(np.linspace(0.15, 0.95, len(edu_madre)))
bars = ax.barh(range(len(edu_madre)), edu_madre.values, color=colores, edgecolor="white")
ax.set_yticks(range(len(edu_madre)))
ax.set_yticklabels(edu_madre.index, fontsize=11)
for i, val in enumerate(edu_madre.values):
    ax.text(val + 1, i, f"{val:.0f}", va="center", fontweight="bold")
ax.set_title("Puntaje Promedio segun Educacion de la Madre", fontsize=15, fontweight="bold")
ax.set_xlabel("Puntaje Promedio", fontsize=12)
plt.tight_layout()
plt.show()

# COMMAND ----------

# --- Top y Bottom 10 departamentos ---
fig, ax = plt.subplots(figsize=(14, 8))
depto = (
    df.groupby("cole_depto_ubicacion")["punt_global"]
    .agg(["mean", "count"])
    .query("count >= 100")
    .sort_values("mean")
)
colores = ["#E53935"] * 5 + ["#9E9E9E"] * (len(depto) - 10) + ["#43A047"] * 5
ax.barh(range(len(depto)), depto["mean"], color=colores, edgecolor="white")
ax.set_yticks(range(len(depto)))
ax.set_yticklabels(depto.index, fontsize=10)
ax.set_title("Puntaje Promedio por Departamento", fontsize=15, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")
plt.tight_layout()
plt.show()

# COMMAND ----------

# --- Puntajes por materia ---
materias = {
    "Matematicas": "punt_matematicas",
    "Lectura Critica": "punt_lectura_critica",
    "C. Naturales": "punt_c_naturales",
    "Sociales": "punt_sociales_ciudadanas",
    "Ingles": "punt_ingles",
}
fig, ax = plt.subplots(figsize=(10, 5))
promedios = pd.Series({k: df[v].mean() for k, v in materias.items()}).sort_values()
promedios.plot(kind="barh", ax=ax, color="#7B1FA2", edgecolor="white")
for i, (idx, val) in enumerate(promedios.items()):
    ax.text(val + 0.3, i, f"{val:.1f}", va="center", fontweight="bold")
ax.set_title("Puntaje Promedio por Materia", fontsize=14, fontweight="bold")
ax.set_xlabel("Puntaje Promedio")
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Guardar datos limpios como tabla Delta

# COMMAND ----------

# Columnas relevantes para el modelo
columnas = [
    "periodo", "estu_genero",
    "cole_area_ubicacion", "cole_bilingue", "cole_naturaleza",
    "cole_jornada", "cole_caracter", "cole_depto_ubicacion",
    "fami_estratovivienda", "fami_educacionmadre", "fami_educacionpadre",
    "fami_personashogar", "fami_tieneautomovil", "fami_tienecomputador",
    "fami_tieneinternet", "fami_tienelavadora",
    "punt_global", "punt_matematicas", "punt_lectura_critica",
    "punt_c_naturales", "punt_sociales_ciudadanas", "punt_ingles",
]

df_limpio = df[[c for c in columnas if c in df.columns]].copy()
spark_df = spark.createDataFrame(df_limpio)
spark_df.write.mode("overwrite").saveAsTable("default.icfes_saber11")
print(f"Tabla 'default.icfes_saber11' guardada: {len(df_limpio):,} filas")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) as total,
# MAGIC        ROUND(AVG(punt_global), 0) as promedio,
# MAGIC        ROUND(MIN(punt_global), 0) as minimo,
# MAGIC        ROUND(MAX(punt_global), 0) as maximo
# MAGIC FROM default.icfes_saber11

# COMMAND ----------

# MAGIC %md
# MAGIC ## Momento IA: Genie Code
# MAGIC
# MAGIC Abre **Genie** en el panel lateral y prueba estas preguntas:
# MAGIC
# MAGIC - "Cual es el puntaje promedio por estrato?"
# MAGIC - "Hay diferencia entre colegios oficiales y privados por departamento?"
# MAGIC - "Que porcentaje de estudiantes de estrato 1 supera los 300 puntos?"
# MAGIC - "Muestra el puntaje de matematicas vs lectura critica"
# MAGIC - "Cuales son los mejores departamentos en ingles?"
# MAGIC
# MAGIC Genie conoce las columnas de tu tabla y genera SQL + graficas automaticamente.
