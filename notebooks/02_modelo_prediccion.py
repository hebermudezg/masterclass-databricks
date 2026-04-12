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

# Veamos los valores unicos de las columnas categoricas clave
for col in ["fami_estratovivienda", "fami_educacionmadre", "cole_naturaleza",
            "cole_area_ubicacion", "cole_bilingue", "estu_genero", "fami_tieneinternet"]:
    print(f"{col}: {sorted(df[col].unique())}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Regresion Lineal
# MAGIC
# MAGIC Empezamos con el modelo mas simple e interpretable.
# MAGIC Los coeficientes nos dicen cuantos puntos sube o baja cada variable.
# MAGIC
# MAGIC > Con el dataframe `df` que ya esta cargado, haz lo siguiente:
# MAGIC >
# MAGIC > 1. Crea nuevas columnas numericas a partir de las categoricas
# MAGIC >    (revisa los valores unicos de la celda anterior para usar
# MAGIC >    los valores exactos en los mapeos):
# MAGIC >    - `estrato`: extraer el numero de `fami_estratovivienda` (1 a 6, Sin Estrato=0)
# MAGIC >    - `edu_madre`: codificar `fami_educacionmadre` de 0 (Ninguno) a 9 (Postgrado) segun nivel
# MAGIC >    - `edu_padre`: igual con `fami_educacionpadre`
# MAGIC >    - `oficial`: 1 si `cole_naturaleza` == "OFICIAL"
# MAGIC >    - `rural`: 1 si `cole_area_ubicacion` == "RURAL"
# MAGIC >    - `bilingue`: 1 si `cole_bilingue` == "S"
# MAGIC >    - `hombre`: 1 si `estu_genero` == "M"
# MAGIC >    - `internet`: 1 si `fami_tieneinternet` == "Si"
# MAGIC >    - `computador`: 1 si `fami_tienecomputador` == "Si"
# MAGIC >    - `automovil`: 1 si `fami_tieneautomovil` == "Si"
# MAGIC >    - `lavadora`: 1 si `fami_tienelavadora` == "Si"
# MAGIC >
# MAGIC > 2. Aplica `.fillna(0)` a todas las columnas nuevas
# MAGIC >
# MAGIC > 3. Define X con las 11 columnas nuevas, y con punt_global
# MAGIC >
# MAGIC > 4. Divide 80/20 con random_state=42
# MAGIC >
# MAGIC > 5. Entrena una Regresion Lineal, imprime MAE y R2
# MAGIC >
# MAGIC > 6. Grafica barras horizontales con los coeficientes del modelo
# MAGIC >    (cuantos puntos aporta cada variable)

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Gradient Boosting + comparacion grafica
# MAGIC
# MAGIC Ahora un modelo mas poderoso. Y comparamos visualmente.
# MAGIC
# MAGIC > Con los mismos datos X_train, y_train, X_test, y_test
# MAGIC > que ya existen de la celda anterior:
# MAGIC >
# MAGIC > 1. Entrena un GradientBoostingRegressor con n_estimators=200,
# MAGIC >    max_depth=5, learning_rate=0.1, random_state=42
# MAGIC >
# MAGIC > 2. Evalua con MAE y R2
# MAGIC >
# MAGIC > 3. Crea una grafica de barras agrupadas comparando
# MAGIC >    Regresion Lineal vs Gradient Boosting (MAE y R2 lado a lado).
# MAGIC >    Indica cual modelo es mejor.
# MAGIC >
# MAGIC > 4. Guarda el mejor modelo con mlflow: usa mlflow.set_experiment,
# MAGIC >    mlflow.start_run, mlflow.sklearn.log_model y mlflow.log_metrics

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Importancia de variables + prediccion
# MAGIC
# MAGIC El momento revelador.
# MAGIC
# MAGIC > Con el modelo Gradient Boosting que acabas de entrenar:
# MAGIC >
# MAGIC > 1. Grafica barras horizontales con la importancia de cada
# MAGIC >    variable, de mayor a menor, con colores de rojo a verde
# MAGIC >
# MAGIC > 2. Predice el puntaje para dos estudiantes usando las mismas
# MAGIC >    columnas de X_train:
# MAGIC >    - Estudiante A: estrato=1, edu_madre=1, edu_padre=1,
# MAGIC >      oficial=1, rural=1, bilingue=0, hombre=0,
# MAGIC >      internet=0, computador=0, automovil=0, lavadora=0
# MAGIC >    - Estudiante B: estrato=5, edu_madre=9, edu_padre=8,
# MAGIC >      oficial=0, rural=0, bilingue=1, hombre=1,
# MAGIC >      internet=1, computador=1, automovil=1, lavadora=1
# MAGIC >
# MAGIC > 3. Imprime ambos puntajes y la diferencia entre ellos

# COMMAND ----------


