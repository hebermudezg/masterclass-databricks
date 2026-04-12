# Databricks notebook source
# MAGIC %md
# MAGIC # Deploy del Modelo a Produccion
# MAGIC
# MAGIC Tomamos el modelo entrenado en el notebook anterior y lo
# MAGIC desplegamos como una **API REST** que cualquier aplicacion
# MAGIC puede consultar.
# MAGIC
# MAGIC **Caso de uso:** Una secretaria de educacion podria usar esta
# MAGIC API para identificar estudiantes en riesgo ANTES del examen
# MAGIC y priorizar recursos de apoyo.
# MAGIC
# MAGIC *Nota: Model Serving puede requerir Databricks Pay-As-You-Go.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Cargar el modelo guardado
# MAGIC
# MAGIC > Busca el ultimo experimento de MLflow, obtiene el run mas
# MAGIC > reciente y carga el modelo guardado. Imprime el run_id
# MAGIC > y las metricas del modelo.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Registrar el modelo
# MAGIC
# MAGIC > Registra el modelo del ultimo run en MLflow Model Registry
# MAGIC > con el nombre "prediccion_icfes".
# MAGIC > Usa mlflow.register_model() con el URI del run.
# MAGIC > Imprime el nombre y la version del modelo registrado.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Crear endpoint de serving
# MAGIC
# MAGIC > Usa el SDK de Databricks (databricks.sdk) para crear un
# MAGIC > endpoint de Model Serving llamado "prediccion-icfes"
# MAGIC > con el modelo registrado. Habilita scale_to_zero_enabled=True
# MAGIC > y workload_size="Small".
# MAGIC >
# MAGIC > Si el endpoint ya existe, actualizalo.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 4: Probar el endpoint
# MAGIC
# MAGIC > Envia una prediccion de prueba al endpoint "prediccion-icfes"
# MAGIC > con dos perfiles de estudiantes:
# MAGIC > - Estudiante A: estrato=1, edu_madre=1, edu_padre=1, oficial=1,
# MAGIC >   rural=1, bilingue=0, hombre=0, internet=0, computador=0,
# MAGIC >   automovil=0, lavadora=0
# MAGIC > - Estudiante B: estrato=5, edu_madre=9, edu_padre=8, oficial=0,
# MAGIC >   rural=0, bilingue=1, hombre=1, internet=1, computador=1,
# MAGIC >   automovil=1, lavadora=1
# MAGIC >
# MAGIC > Muestra los puntajes predichos y la diferencia.
# MAGIC > Tambien muestra el curl de ejemplo para llamar la API externamente.

# COMMAND ----------


