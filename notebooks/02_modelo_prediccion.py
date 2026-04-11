# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a entrenar modelos de machine learning para predecir el
# MAGIC puntaje del ICFES usando **solo variables socioeconomicas**.
# MAGIC
# MAGIC Le pedimos al asistente de IA que nos escriba el codigo paso a paso.

# COMMAND ----------

import pandas as pd

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes")
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Regresion Lineal
# MAGIC
# MAGIC Empezamos con el modelo mas simple e interpretable.
# MAGIC Los coeficientes nos dicen cuantos puntos sube o baja cada variable.
# MAGIC
# MAGIC > Del dataframe `df`, necesito predecir `punt_global` con una Regresion Lineal.
# MAGIC >
# MAGIC > Primero imprime los valores unicos de `fami_estratovivienda`,
# MAGIC > `fami_educacionmadre` y `fami_educacionpadre` para ver que contienen.
# MAGIC >
# MAGIC > Luego codifica todas las columnas categoricas como numeros:
# MAGIC > - `fami_estratovivienda`: ordinal donde Estrato 1=1 hasta Estrato 6=6,
# MAGIC >   usa los valores exactos que viste en el unique()
# MAGIC > - `fami_educacionmadre` y `fami_educacionpadre`: ordinal de menor a mayor
# MAGIC >   nivel educativo, usa los valores exactos que viste en el unique()
# MAGIC > - Las columnas binarias (`cole_naturaleza`, `cole_area_ubicacion`,
# MAGIC >   `cole_bilingue`, `estu_genero`, `fami_tieneinternet`,
# MAGIC >   `fami_tienecomputador`, `fami_tieneautomovil`, `fami_tienelavadora`):
# MAGIC >   convierte a 1/0
# MAGIC >
# MAGIC > Aplica fillna(0) para evitar errores.
# MAGIC > Divide 80/20 con random_state=42.
# MAGIC > Entrena la Regresion Lineal, muestra MAE y R2.
# MAGIC > Grafica barras horizontales con los coeficientes (cuantos puntos
# MAGIC > aporta cada variable).

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Gradient Boosting + comparacion grafica
# MAGIC
# MAGIC Ahora un modelo mas poderoso. Y comparamos visualmente.
# MAGIC
# MAGIC > Con los mismos datos (X_train, y_train, X_test, y_test),
# MAGIC > entrena un **GradientBoostingRegressor** con 200 estimators,
# MAGIC > max_depth=5, learning_rate=0.1, random_state=42.
# MAGIC >
# MAGIC > Compara los dos modelos (Regresion Lineal vs Gradient Boosting)
# MAGIC > en una **grafica de barras agrupadas** mostrando MAE y R2
# MAGIC > de cada uno. Pon titulo y etiquetas claras. Indica el ganador.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Importancia de variables + prediccion de perfiles
# MAGIC
# MAGIC El momento revelador: que factores pesan mas y cuanto
# MAGIC cambia la prediccion entre dos estudiantes diferentes.
# MAGIC
# MAGIC > Con el modelo Gradient Boosting:
# MAGIC >
# MAGIC > 1. Crea una grafica de barras horizontales con la importancia
# MAGIC >    de cada variable, ordenada de mayor a menor, con colores
# MAGIC >    que vayan de rojo (menos importante) a verde (mas importante)
# MAGIC >
# MAGIC > 2. Predice el puntaje para dos estudiantes:
# MAGIC >    - Estudiante A: estrato=1, edu_madre=1 (primaria incompleta),
# MAGIC >      edu_padre=1, oficial=1, rural=1, bilingue=0, hombre=0,
# MAGIC >      internet=0, computador=0, automovil=0, lavadora=0
# MAGIC >    - Estudiante B: estrato=5, edu_madre=9 (postgrado),
# MAGIC >      edu_padre=8, oficial=0, rural=0, bilingue=1, hombre=1,
# MAGIC >      internet=1, computador=1, automovil=1, lavadora=1
# MAGIC >
# MAGIC > 3. Imprime los puntajes predichos y la diferencia

# COMMAND ----------


