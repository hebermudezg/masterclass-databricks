# Databricks notebook source
# MAGIC %md
# MAGIC # Deploy del Modelo a Produccion
# MAGIC
# MAGIC Desplegamos el modelo de prediccion del ICFES como una **API REST**.
# MAGIC
# MAGIC **Caso de uso real:** El Ministerio de Educacion podria usar un modelo asi
# MAGIC para identificar estudiantes en riesgo ANTES del examen y priorizar
# MAGIC recursos de apoyo donde mas se necesitan.
# MAGIC
# MAGIC **Nota:** Model Serving requiere Databricks Pay-As-You-Go.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Verificar modelo registrado

# COMMAND ----------

import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_registry_uri("databricks-uc")
client = MlflowClient(registry_uri="databricks-uc")
modelo_nombre = "main.default.prediccion_icfes_saber11"

versiones = client.search_model_versions(f"name='{modelo_nombre}'")
ultima = max(versiones, key=lambda v: int(v.version))

print(f"Modelo: {modelo_nombre}")
print(f"Version: {ultima.version}")
print(f"Estado: {ultima.status}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Crear endpoint de serving

# COMMAND ----------

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointCoreConfigInput, ServedEntityInput

w = WorkspaceClient()
endpoint_name = "prediccion-icfes"

try:
    w.serving_endpoints.create_and_wait(
        name=endpoint_name,
        config=EndpointCoreConfigInput(
            served_entities=[
                ServedEntityInput(
                    entity_name=modelo_nombre,
                    entity_version=ultima.version,
                    workload_size="Small",
                    scale_to_zero_enabled=True,
                )
            ]
        ),
    )
    print(f"Endpoint '{endpoint_name}' creado y listo")
except Exception as e:
    if "already exists" in str(e).lower():
        print(f"Endpoint ya existe, actualizando...")
        w.serving_endpoints.update_config_and_wait(
            name=endpoint_name,
            served_entities=[
                ServedEntityInput(
                    entity_name=modelo_nombre,
                    entity_version=ultima.version,
                    workload_size="Small",
                    scale_to_zero_enabled=True,
                )
            ],
        )
        print("Endpoint actualizado")
    else:
        raise e

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Probar con predicciones reales

# COMMAND ----------

# Dos estudiantes con perfiles contrastantes
datos_prueba = {
    "dataframe_records": [
        {
            "estrato_cod": 1, "edu_madre_cod": 1, "edu_padre_cod": 1,
            "colegio_oficial": 1, "colegio_rural": 1, "colegio_bilingue": 0,
            "genero_m": 0, "tiene_internet": 0, "tiene_computador": 0,
            "tiene_automovil": 0, "tiene_lavadora": 0, "personas_hogar_cod": 3,
        },
        {
            "estrato_cod": 5, "edu_madre_cod": 9, "edu_padre_cod": 8,
            "colegio_oficial": 0, "colegio_rural": 0, "colegio_bilingue": 1,
            "genero_m": 1, "tiene_internet": 1, "tiene_computador": 1,
            "tiene_automovil": 1, "tiene_lavadora": 1, "personas_hogar_cod": 2,
        },
    ]
}

respuesta = w.serving_endpoints.query(
    name=endpoint_name,
    dataframe_records=datos_prueba["dataframe_records"],
)

perfiles = [
    "Estrato 1 | Oficial Rural | Sin internet | Mama: Primaria",
    "Estrato 5 | Privado Bilingue | Con internet | Mama: Postgrado",
]

print("Predicciones del modelo EN PRODUCCION:")
print("=" * 60)
for perfil, pred in zip(perfiles, respuesta.predictions):
    print(f"  {perfil}")
    print(f"  -> Puntaje predicho: {pred:.0f}")
    print()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Usar desde cualquier aplicacion
# MAGIC
# MAGIC El modelo es ahora una API REST:
# MAGIC
# MAGIC ```bash
# MAGIC curl -X POST \
# MAGIC   https://<tu-workspace>.databricks.net/serving-endpoints/prediccion-icfes/invocations \
# MAGIC   -H "Authorization: Bearer <tu-token>" \
# MAGIC   -H "Content-Type: application/json" \
# MAGIC   -d '{
# MAGIC     "dataframe_records": [{
# MAGIC       "estrato_cod": 3,
# MAGIC       "edu_madre_cod": 4,
# MAGIC       "edu_padre_cod": 4,
# MAGIC       "colegio_oficial": 1,
# MAGIC       "colegio_rural": 0,
# MAGIC       "colegio_bilingue": 0,
# MAGIC       "genero_m": 1,
# MAGIC       "tiene_internet": 1,
# MAGIC       "tiene_computador": 1,
# MAGIC       "tiene_automovil": 0,
# MAGIC       "tiene_lavadora": 1,
# MAGIC       "personas_hogar_cod": 2
# MAGIC     }]
# MAGIC   }'
# MAGIC ```
# MAGIC
# MAGIC **Caso real:** Una secretaria de educacion podria integrar esto en su
# MAGIC plataforma para identificar estudiantes en riesgo y asignar tutores.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Limpiar recursos

# COMMAND ----------

# Descomenta para eliminar el endpoint y dejar de pagar:
# w.serving_endpoints.delete(name=endpoint_name)
# print(f"Endpoint '{endpoint_name}' eliminado")
