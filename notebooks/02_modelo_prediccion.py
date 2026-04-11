# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a pedirle al asistente de IA de Databricks que nos
# MAGIC entrene un modelo de machine learning para predecir el
# MAGIC puntaje del ICFES usando solo variables socioeconomicas.

# COMMAND ----------

import pandas as pd

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes")
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Entrenar el modelo con ayuda de la IA
# MAGIC
# MAGIC Ahora le pedimos al **Databricks Assistant** que nos escriba todo
# MAGIC el codigo de machine learning. Hacemos click en la celda de abajo,
# MAGIC abrimos el Assistant, y le damos este prompt:
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC > Tengo un dataframe llamado `df` con resultados del examen ICFES Saber 11
# MAGIC > de Colombia. Entrena un modelo **Random Forest** para predecir la columna
# MAGIC > `punt_global` usando estas variables socioeconomicas:
# MAGIC > `fami_estratovivienda`, `fami_educacionmadre`, `fami_educacionpadre`,
# MAGIC > `cole_naturaleza`, `cole_area_ubicacion`, `cole_bilingue`,
# MAGIC > `estu_genero`, `fami_tieneinternet`, `fami_tienecomputador`,
# MAGIC > `fami_tieneautomovil`, `fami_tienelavadora`.
# MAGIC >
# MAGIC > Pasos:
# MAGIC > 1. Codifica las columnas categoricas como numeros (ordinal para estrato 1-6
# MAGIC >    y niveles de educacion, binario para columnas Si/No)
# MAGIC > 2. Divide 80/20 train/test con random_state=42
# MAGIC > 3. Entrena un RandomForestRegressor con 200 estimators
# MAGIC > 4. Imprime el MAE y el R2 score
# MAGIC > 5. Grafica un bar chart horizontal con la importancia de cada variable
# MAGIC > 6. Predice para dos estudiantes contrastantes:
# MAGIC >    - Estudiante A: Estrato 1, colegio oficial rural, mama con primaria, sin internet
# MAGIC >    - Estudiante B: Estrato 5, colegio privado bilingue, mama con postgrado, con internet
# MAGIC > 7. Muestra la diferencia en puntaje predicho
# MAGIC > 8. Registra el modelo en MLflow con `mlflow.set_registry_uri("databricks-uc")`
# MAGIC >    y `mlflow.register_model()` con el nombre `main.default.prediccion_icfes_saber11`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC *Si el codigo se corta, escribir "continue" en la siguiente celda.
# MAGIC Si da error, seleccionar el error y pedir "fix this".*

# COMMAND ----------


