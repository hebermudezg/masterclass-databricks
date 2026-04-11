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
# MAGIC > I have a dataframe called `df` with Colombian ICFES exam results.
# MAGIC > Train a **Random Forest** model to predict the column `punt_global`
# MAGIC > using these socioeconomic features:
# MAGIC > `fami_estratovivienda`, `fami_educacionmadre`, `fami_educacionpadre`,
# MAGIC > `cole_naturaleza`, `cole_area_ubicacion`, `cole_bilingue`,
# MAGIC > `estu_genero`, `fami_tieneinternet`, `fami_tienecomputador`,
# MAGIC > `fami_tieneautomovil`, `fami_tienelavadora`.
# MAGIC >
# MAGIC > Steps:
# MAGIC > 1. Encode categorical columns as numeric (ordinal for estrato 1-6
# MAGIC >    and education levels, binary for yes/no columns)
# MAGIC > 2. Split 80/20 train/test with random_state=42
# MAGIC > 3. Train a RandomForestRegressor with 200 estimators
# MAGIC > 4. Print MAE and R2 score
# MAGIC > 5. Plot a horizontal bar chart of feature importances
# MAGIC > 6. Predict for two contrasting students:
# MAGIC >    - Student A: Estrato 1, public rural school, mother primary education, no internet
# MAGIC >    - Student B: Estrato 5, private bilingual school, mother postgraduate, with internet
# MAGIC > 7. Show the difference in predicted scores
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC *Tip: el Assistant funciona mejor con prompts en ingles.
# MAGIC Si el codigo se corta, escribir "continue" en la siguiente celda.
# MAGIC Si da error, seleccionar el error y pedir "fix this".*

# COMMAND ----------


