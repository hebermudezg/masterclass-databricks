# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a entrenar un modelo que prediga el puntaje del ICFES
# MAGIC usando **solo variables socioeconomicas**.
# MAGIC
# MAGIC Ninguna variable academica. Solo contexto.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 1
# MAGIC Carga los datos de la tabla Delta `default.icfes_saber11` como DataFrame de pandas.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 2
# MAGIC Necesitamos convertir las variables categoricas a numeros para que el modelo pueda procesarlas:
# MAGIC
# MAGIC - `fami_estratovivienda` → numero del 1 al 6
# MAGIC - `fami_educacionmadre` y `fami_educacionpadre` → escala del 0 (ninguno) al 9 (postgrado)
# MAGIC - `cole_naturaleza`, `cole_area_ubicacion`, `cole_bilingue`, `estu_genero`, `fami_tieneinternet`, `fami_tienecomputador`, `fami_tieneautomovil`, `fami_tienelavadora` → 1 o 0

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 3
# MAGIC Entrena un modelo **Random Forest** para predecir `punt_global`
# MAGIC usando las variables socioeconomicas que acabamos de crear.
# MAGIC
# MAGIC Divide los datos en 80% entrenamiento y 20% prueba.
# MAGIC Usa `mlflow.autolog()` para registrar el experimento automaticamente.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 4
# MAGIC Evalua el modelo: muestra el error promedio (MAE)
# MAGIC y que porcentaje de la variacion explica (R2).

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 5
# MAGIC Crea una grafica de barras horizontales mostrando la
# MAGIC **importancia de cada variable** en la prediccion.
# MAGIC
# MAGIC Esto nos dice: que factores pesan mas en el puntaje del ICFES?

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 6
# MAGIC Predice el puntaje para dos perfiles contrastantes:
# MAGIC
# MAGIC **Perfil A:** Estrato 1, colegio oficial rural, mama con primaria, sin internet, sin computador
# MAGIC
# MAGIC **Perfil B:** Estrato 5, colegio privado bilingue, mama con postgrado, con internet y computador
# MAGIC
# MAGIC Muestra la diferencia en puntos.

# COMMAND ----------


