# Databricks notebook source
# MAGIC %md
# MAGIC # Deploy del Modelo a Produccion
# MAGIC
# MAGIC Tomamos el modelo **prediccion_icfes** guardado en el notebook
# MAGIC anterior y lo desplegamos como API REST.
# MAGIC
# MAGIC *Model Serving puede requerir Databricks Pay-As-You-Go.*

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 1: Cargar el modelo "prediccion_icfes" de MLflow
# MAGIC
# MAGIC > Busca en MLflow el modelo registrado con nombre "prediccion_icfes".
# MAGIC > Usa mlflow.MlflowClient() para obtener la ultima version del modelo.
# MAGIC > Carga el modelo con mlflow.sklearn.load_model() usando el source
# MAGIC > de la ultima version.
# MAGIC > Imprime: nombre del modelo, version, run_id, y las metricas
# MAGIC > (mae y r2) del run asociado.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Crear endpoint de serving
# MAGIC
# MAGIC > Usa databricks.sdk.WorkspaceClient para crear un endpoint
# MAGIC > de Model Serving:
# MAGIC > - Nombre del endpoint: "prediccion-icfes"
# MAGIC > - Modelo: "prediccion_icfes" (el que acabamos de cargar)
# MAGIC > - Version: la ultima version obtenida en el paso anterior
# MAGIC > - workload_size: "Small"
# MAGIC > - scale_to_zero_enabled: True
# MAGIC >
# MAGIC > Si el endpoint ya existe, actualizalo en vez de crearlo.
# MAGIC > Usa create_and_wait o update_config_and_wait para esperar
# MAGIC > a que este listo. Imprime el estado del endpoint.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 3: Probar la API con dos perfiles
# MAGIC
# MAGIC > Envia una solicitud al endpoint "prediccion-icfes" con
# MAGIC > w.serving_endpoints.query(). Enviar dos registros:
# MAGIC >
# MAGIC > Estudiante A: estrato=1, edu_madre=1, edu_padre=1, oficial=1,
# MAGIC >   rural=1, bilingue=0, hombre=0, internet=0, computador=0,
# MAGIC >   automovil=0, lavadora=0
# MAGIC >
# MAGIC > Estudiante B: estrato=5, edu_madre=9, edu_padre=8, oficial=0,
# MAGIC >   rural=0, bilingue=1, hombre=1, internet=1, computador=1,
# MAGIC >   automovil=1, lavadora=1
# MAGIC >
# MAGIC > Imprimir los puntajes predichos y la diferencia.
# MAGIC >
# MAGIC > Tambien generar el comando curl equivalente para llamar la API
# MAGIC > desde fuera de Databricks, usando el workspace URL actual y
# MAGIC > un placeholder para el token.

# COMMAND ----------


