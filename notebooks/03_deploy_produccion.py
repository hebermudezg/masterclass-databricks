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
# MAGIC > tres estudiantes. El modelo espera un DataFrame con estas
# MAGIC > columnas exactas: fami_estratovivienda, fami_educacionmadre,
# MAGIC > fami_educacionpadre, cole_naturaleza, cole_area_ubicacion,
# MAGIC > cole_bilingue, estu_genero, fami_tieneinternet,
# MAGIC > fami_tienecomputador, fami_tieneautomovil, fami_tienelavadora.
# MAGIC >
# MAGIC > Los perfiles:
# MAGIC > - Estudiante A: fami_estratovivienda="Estrato 1",
# MAGIC >   fami_educacionmadre="Primaria incompleta",
# MAGIC >   fami_educacionpadre="Primaria incompleta",
# MAGIC >   cole_naturaleza="OFICIAL", cole_area_ubicacion="RURAL",
# MAGIC >   cole_bilingue="N", estu_genero="F",
# MAGIC >   fami_tieneinternet="No", fami_tienecomputador="No",
# MAGIC >   fami_tieneautomovil="No", fami_tienelavadora="No"
# MAGIC > - Estudiante B: fami_estratovivienda="Estrato 5",
# MAGIC >   fami_educacionmadre="Postgrado",
# MAGIC >   fami_educacionpadre="Educación profesional completa",
# MAGIC >   cole_naturaleza="NO OFICIAL", cole_area_ubicacion="URBANO",
# MAGIC >   cole_bilingue="S", estu_genero="M",
# MAGIC >   fami_tieneinternet="Si", fami_tienecomputador="Si",
# MAGIC >   fami_tieneautomovil="Si", fami_tienelavadora="Si"
# MAGIC > - Estudiante C: fami_estratovivienda="Estrato 3",
# MAGIC >   fami_educacionmadre="Secundaria (Bachillerato) completa",
# MAGIC >   fami_educacionpadre="Secundaria (Bachillerato) completa",
# MAGIC >   cole_naturaleza="OFICIAL", cole_area_ubicacion="URBANO",
# MAGIC >   cole_bilingue="N", estu_genero="M",
# MAGIC >   fami_tieneinternet="Si", fami_tienecomputador="No",
# MAGIC >   fami_tieneautomovil="No", fami_tienelavadora="Si"
# MAGIC >
# MAGIC > Muestra los puntajes predichos y una grafica de barras
# MAGIC > comparando los tres perfiles.

# COMMAND ----------


