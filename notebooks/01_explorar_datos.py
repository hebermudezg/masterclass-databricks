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

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Explorar con Genie
# MAGIC
# MAGIC **Genie** es el asistente de IA de Databricks. Permite hacer preguntas
# MAGIC sobre los datos en lenguaje natural, sin escribir codigo.
# MAGIC
# MAGIC **Como funciona:**
# MAGIC 1. Le escribes una pregunta en espanol (como si hablaras con un colega)
# MAGIC 2. Genie genera el SQL necesario automaticamente
# MAGIC 3. Ejecuta la consulta contra la tabla Delta
# MAGIC 4. Muestra el resultado con visualizacion incluida
# MAGIC
# MAGIC Genie conoce la estructura de la tabla: sabe que columnas existen,
# MAGIC que tipo de datos tiene cada una y que valores son posibles.
# MAGIC No hay que explicarle el esquema, el lo descubre solo.
# MAGIC
# MAGIC **Para usarlo:** Menu lateral > **Genie** > seleccionar `default.icfes_saber11`
# MAGIC
# MAGIC **Preguntas de ejemplo:**
# MAGIC - Cuantos estudiantes hay por estrato?
# MAGIC - Cual es el puntaje promedio por estrato socioeconomico?
# MAGIC - Hay diferencia entre colegios oficiales y privados?
# MAGIC - Los estudiantes con internet tienen mejor puntaje?
# MAGIC - Como afecta la educacion de la madre al puntaje?
# MAGIC - Cuales son los 10 mejores departamentos?
# MAGIC - Que porcentaje de estrato 1 supera los 300 puntos?
