# Databricks notebook source
# MAGIC %md
# MAGIC # Cargar y usar el modelo guardado
# MAGIC
# MAGIC Cargamos el modelo entrenado en el notebook anterior desde MLflow
# MAGIC y lo usamos para hacer predicciones.

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 1: Cargar el modelo desde MLflow
# MAGIC
# MAGIC > En el notebook anterior guarde un modelo en MLflow.
# MAGIC > No tengo Unity Catalog habilitado.
# MAGIC > Busca el modelo en MLflow Experiments usando
# MAGIC > mlflow.set_registry_uri("databricks") y search_runs().
# MAGIC > Carga el modelo del run mas reciente e imprime el run_id.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Predecir para distintos perfiles de estudiantes
# MAGIC
# MAGIC > Con el modelo cargado, predice el puntaje del ICFES para
# MAGIC > estos tres estudiantes. Crea un DataFrame con las mismas
# MAGIC > columnas que el modelo espera (las del notebook anterior):
# MAGIC >
# MAGIC > - Estudiante A: Estrato 1, colegio oficial rural, mama con
# MAGIC >   primaria incompleta, sin internet, sin computador
# MAGIC > - Estudiante B: Estrato 5, colegio privado bilingue urbano,
# MAGIC >   mama con postgrado, con internet y computador
# MAGIC > - Estudiante C: Estrato 3, colegio oficial urbano, mama
# MAGIC >   con bachillerato completo, con internet, sin computador
# MAGIC >
# MAGIC > Muestra los puntajes predichos y una grafica de barras
# MAGIC > comparando los tres perfiles.

# COMMAND ----------


