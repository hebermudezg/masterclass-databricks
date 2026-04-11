# Databricks notebook source
# MAGIC %md
# MAGIC # ICFES Saber 11: Analitica Asistida por IA
# MAGIC
# MAGIC > **Puede la IA predecir tu puntaje del ICFES solo con saber
# MAGIC > tu estrato, tipo de colegio y si tienes internet en casa?**
# MAGIC
# MAGIC **Dataset:** 7+ millones de resultados reales del Saber 11
# MAGIC **Fuente:** [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe)
# MAGIC
# MAGIC **Flujo de este notebook:**
# MAGIC 1. Cargamos los datos y los preparamos
# MAGIC 2. Los guardamos como **tabla Delta** (para que Genie pueda acceder)
# MAGIC 3. Exploramos con **Genie** - la IA de Databricks genera SQL por nosotros
# MAGIC 4. Creamos visualizaciones avanzadas con Python

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Paso 1: Cargar datos del ICFES
# MAGIC
# MAGIC Descargamos resultados recientes directamente desde el portal
# MAGIC de datos abiertos del gobierno colombiano.

# COMMAND ----------

import pandas as pd
import numpy as np

URL_DATOS = (
    "https://www.datos.gov.co/resource/kgxf-xxbe.csv"
    "?$limit=50000"
    "&$where=punt_global%20IS%20NOT%20NULL%20AND%20periodo%20%3E%3D%20%2720201%27"
    "&$order=periodo%20DESC"
)

# Alternativa: si pre-subiste el CSV a un Volume
# URL_DATOS = "/Volumes/main/default/raw_data/icfes_saber11.csv"

print("Descargando resultados del ICFES Saber 11 desde datos.gov.co...")
df = pd.read_csv(URL_DATOS)
print(f"Dataset cargado: {df.shape[0]:,} filas x {df.shape[1]} columnas")

# COMMAND ----------

df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Paso 2: Limpieza rapida
# MAGIC
# MAGIC Tres cosas basicas: quitar duplicados, convertir puntajes a numeros,
# MAGIC y filtrar registros validos.

# COMMAND ----------

# Eliminar duplicados (hay filas repetidas en el dataset original)
antes = len(df)
df = df.drop_duplicates(subset=["estu_consecutivo"], keep="first")
print(f"Duplicados eliminados: {antes - len(df):,}")

# Convertir puntajes de texto a numerico
cols_puntaje = ["punt_global", "punt_matematicas", "punt_lectura_critica",
                "punt_c_naturales", "punt_sociales_ciudadanas", "punt_ingles"]
for col in cols_puntaje:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["punt_global"])
print(f"Registros listos: {len(df):,}")
print(f"Puntaje promedio: {df['punt_global'].mean():.0f} | Mediana: {df['punt_global'].median():.0f}")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Paso 3: Guardar como tabla Delta
# MAGIC
# MAGIC ### Que es una tabla Delta?
# MAGIC
# MAGIC **Delta Lake** es el formato nativo de almacenamiento de Databricks.
# MAGIC Piensen en ello como una tabla de base de datos inteligente:
# MAGIC
# MAGIC - Se guarda en formato optimizado (Parquet + log de transacciones)
# MAGIC - Permite consultas SQL rapidas sobre millones de filas
# MAGIC - Tiene versionado automatico (puedes "viajar en el tiempo" a versiones anteriores)
# MAGIC - Y lo mas importante para nosotros: **Genie puede consultarla con lenguaje natural**
# MAGIC
# MAGIC Al guardar nuestros datos como tabla Delta, desbloqueamos toda la
# MAGIC inteligencia artificial de Databricks sobre ellos.

# COMMAND ----------

# Seleccionamos las columnas que nos interesan
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
print(f"Tabla Delta 'default.icfes_saber11' guardada: {len(df_limpio):,} filas")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verificamos que la tabla quedo bien
# MAGIC SELECT COUNT(*) as total_estudiantes,
# MAGIC        ROUND(AVG(punt_global), 0) as puntaje_promedio,
# MAGIC        ROUND(MIN(punt_global), 0) as puntaje_minimo,
# MAGIC        ROUND(MAX(punt_global), 0) as puntaje_maximo
# MAGIC FROM default.icfes_saber11

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Paso 4: Explorar con Genie (SIN escribir codigo)
# MAGIC
# MAGIC Ahora viene lo interesante. Vamos a abrir **Genie**, el asistente de IA
# MAGIC de Databricks, y le vamos a hacer preguntas a los datos en lenguaje natural.
# MAGIC
# MAGIC **Como abrir Genie:**
# MAGIC - En el menu lateral izquierdo, click en **"Genie"** (bajo la seccion SQL)
# MAGIC - Selecciona la tabla `default.icfes_saber11`
# MAGIC - Empieza a preguntar
# MAGIC
# MAGIC Genie genera SQL automaticamente. No necesitas saber SQL - solo preguntar.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Preguntas sugeridas (seguir este orden para contar una historia)
# MAGIC
# MAGIC **Calentamiento - conocer los datos:**
# MAGIC
# MAGIC 1. `Cuantos estudiantes hay en total?`
# MAGIC 2. `Cual es el puntaje global promedio?`
# MAGIC 3. `Cuantos estudiantes hay por estrato?`
# MAGIC
# MAGIC **El descubrimiento principal - la desigualdad:**
# MAGIC
# MAGIC 4. `Cual es el puntaje promedio por estrato socioeconomico?`
# MAGIC    *(Este es el momento clave. Dejar que la audiencia reaccione.)*
# MAGIC
# MAGIC 5. `Hay diferencia de puntaje entre colegios OFICIAL y NO OFICIAL?`
# MAGIC 6. `Los estudiantes con internet en casa tienen mejor puntaje?`
# MAGIC 7. `Como afecta la educacion de la madre al puntaje?`
# MAGIC
# MAGIC **Profundizando - preguntas mas especificas:**
# MAGIC
# MAGIC 8. `Que porcentaje de estudiantes de Estrato 1 supera los 300 puntos?`
# MAGIC 9. `Cuales son los 10 departamentos con mejor puntaje promedio?`
# MAGIC 10. `Cual es el puntaje promedio de ingles por estrato?`
# MAGIC
# MAGIC **Momento audiencia:**
# MAGIC
# MAGIC 11. Preguntar al publico: *"Que quieren saber de los datos?"*
# MAGIC     Escribir en Genie lo que digan. Este es el momento mas interactivo.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Reflexion despues de Genie:**
# MAGIC *"Acabamos de analizar datos de miles de estudiantes colombianos
# MAGIC sin escribir una sola linea de codigo. Genie genero todo el SQL
# MAGIC por nosotros. Eso es analitica asistida por IA."*

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Paso 5: Visualizaciones avanzadas con Python
# MAGIC
# MAGIC Genie es excelente para explorar rapido. Pero para graficas
# MAGIC pulidas, con control total sobre colores, formato y detalle,
# MAGIC usamos Python. Veamos los mismos insights pero con nivel de publicacion.

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

# --- 4 comparaciones clave en un solo panel ---
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

# --- Ranking de departamentos ---
fig, ax = plt.subplots(figsize=(14, 8))
depto = (
    df.groupby("cole_depto_ubicacion")["punt_global"]
    .agg(["mean", "count"])
    .query("count >= 100")
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

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Resumen
# MAGIC
# MAGIC **Con Genie (sin codigo)** descubrimos los patrones principales:
# MAGIC estrato, tipo de colegio, internet y educacion de los padres impactan el puntaje.
# MAGIC
# MAGIC **Con Python** los presentamos de forma profesional y detallada.
# MAGIC
# MAGIC **Siguiente paso:** Notebook 02 - Entrenar un modelo de ML que prediga
# MAGIC el puntaje usando solo estas variables socioeconomicas.
