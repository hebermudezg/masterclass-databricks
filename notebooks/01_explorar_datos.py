# Databricks notebook source
# MAGIC %md
# MAGIC # ICFES Saber 11: Analitica de Datos Asistida por IA
# MAGIC
# MAGIC 27,000+ resultados reales del examen Saber 11
# MAGIC
# MAGIC **Fuente:** [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Cargar los datos

# COMMAND ----------

import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/hebermudezg/masterclass-databricks/main/dataset/icfes_saber11.csv"
)
print(f"{df.shape[0]:,} estudiantes x {df.shape[1]} variables")

# COMMAND ----------

df.head(10)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Guardar como tabla Delta
# MAGIC
# MAGIC **Delta Lake** es el formato de almacenamiento nativo de Databricks.
# MAGIC Al guardar como tabla Delta, herramientas como Genie y el Editor SQL
# MAGIC pueden consultar los datos directamente.

# COMMAND ----------

spark.createDataFrame(df).write.mode("overwrite").saveAsTable("default.icfes_saber11")
print("Tabla Delta creada: default.icfes_saber11")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) as estudiantes,
# MAGIC        ROUND(AVG(punt_global)) as puntaje_promedio,
# MAGIC        MIN(punt_global) as minimo,
# MAGIC        MAX(punt_global) as maximo
# MAGIC FROM default.icfes_saber11
