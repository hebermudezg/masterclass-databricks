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
# MAGIC > Busca el ultimo run de MLflow en este workspace con
# MAGIC > mlflow.search_runs() ordenado por fecha. Carga el modelo
# MAGIC > guardado en ese run. Imprime el run_id y las metricas.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Hacer predicciones con el modelo cargado
# MAGIC
# MAGIC > Con el modelo cargado, predice el puntaje para estos perfiles
# MAGIC > de estudiantes (usa las mismas columnas que el modelo espera):
# MAGIC >
# MAGIC > - Estudiante A: Estrato 1, colegio oficial rural, mama con
# MAGIC >   primaria incompleta, sin internet, sin computador
# MAGIC > - Estudiante B: Estrato 5, colegio privado bilingue urbano,
# MAGIC >   mama con postgrado, con internet y computador
# MAGIC > - Estudiante C: Estrato 3, colegio oficial urbano, mama
# MAGIC >   bachiller, con internet, sin computador
# MAGIC >
# MAGIC > Muestra los puntajes predichos y una grafica de barras
# MAGIC > comparando los tres perfiles.

# COMMAND ----------


