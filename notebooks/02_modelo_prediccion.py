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
# MAGIC Los coeficientes nos dicen cuantos puntos sube o baja
# MAGIC cada variable.
# MAGIC
# MAGIC > Del dataframe `df`, codifica como numeros estas columnas:
# MAGIC > - `fami_estratovivienda`: ordinal de 0 (Sin Estrato) a 6 (Estrato 6)
# MAGIC > - `fami_educacionmadre` y `fami_educacionpadre`: ordinal de 0 (Ninguno) a 9 (Postgrado)
# MAGIC > - `cole_naturaleza`: 1 si es OFICIAL, 0 si no
# MAGIC > - `cole_area_ubicacion`: 1 si es RURAL, 0 si no
# MAGIC > - `cole_bilingue`: 1 si es S, 0 si no
# MAGIC > - `estu_genero`: 1 si es M, 0 si no
# MAGIC > - `fami_tieneinternet`, `fami_tienecomputador`, `fami_tieneautomovil`, `fami_tienelavadora`: 1 si es Si, 0 si no
# MAGIC >
# MAGIC > Divide 80/20 con random_state=42.
# MAGIC > Entrena una **Regresion Lineal** para predecir `punt_global`.
# MAGIC > Muestra el MAE, R2, y una grafica de barras horizontales con
# MAGIC > los coeficientes del modelo (cuantos puntos aporta cada variable).

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


