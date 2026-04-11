# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a pedirle al asistente de IA que nos entrene modelos
# MAGIC de machine learning para predecir el puntaje del ICFES
# MAGIC usando solo variables socioeconomicas.

# COMMAND ----------

import pandas as pd

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes")
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Entrenar un Random Forest
# MAGIC
# MAGIC > Tengo un dataframe `df` con resultados del ICFES Saber 11.
# MAGIC > Codifica como numeros estas columnas categoricas:
# MAGIC > `fami_estratovivienda` (ordinal 1-6), `fami_educacionmadre` y
# MAGIC > `fami_educacionpadre` (ordinal 0-9 de Ninguno a Postgrado),
# MAGIC > `cole_naturaleza`, `cole_area_ubicacion`, `cole_bilingue`,
# MAGIC > `estu_genero`, `fami_tieneinternet`, `fami_tienecomputador`,
# MAGIC > `fami_tieneautomovil`, `fami_tienelavadora` (binario 1/0).
# MAGIC >
# MAGIC > Divide 80/20 con random_state=42. Entrena un RandomForestRegressor
# MAGIC > con 200 estimators para predecir `punt_global`.
# MAGIC > Imprime MAE y R2. Guarda el modelo en una variable llamada `modelo_rf`.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Entrenar un Gradient Boosting y comparar
# MAGIC
# MAGIC > Ahora entrena un GradientBoostingRegressor con los mismos datos
# MAGIC > (X_train, y_train) para predecir `punt_global`.
# MAGIC > Guarda el modelo en `modelo_gb`.
# MAGIC > Evalua con MAE y R2 sobre X_test.
# MAGIC > Compara los dos modelos (Random Forest vs Gradient Boosting)
# MAGIC > en una tabla e indica cual es mejor.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Importancia de variables, prediccion y registro
# MAGIC
# MAGIC > Con el mejor modelo de los dos, haz lo siguiente:
# MAGIC > 1. Grafica un bar chart horizontal con la importancia de cada variable
# MAGIC > 2. Predice el puntaje para dos estudiantes:
# MAGIC >    - Estudiante A: Estrato 1, colegio oficial rural, mama primaria, sin internet
# MAGIC >    - Estudiante B: Estrato 5, colegio privado bilingue, mama postgrado, con internet
# MAGIC > 3. Muestra la diferencia en puntaje
# MAGIC > 4. Registra el modelo en MLflow con:
# MAGIC >    `mlflow.set_registry_uri("databricks-uc")`
# MAGIC >    y nombre `main.default.prediccion_icfes_saber11`

# COMMAND ----------


