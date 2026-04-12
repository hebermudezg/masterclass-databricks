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
print(f"{df.shape[0]:,} estudiantes, {df.shape[1]} columnas")
df.head()

# COMMAND ----------

# Veamos los valores reales de las columnas que vamos a codificar
for col in ["fami_estratovivienda", "fami_educacionmadre", "cole_naturaleza",
            "cole_area_ubicacion", "cole_bilingue", "estu_genero", "fami_tieneinternet"]:
    print(f"\n{col}:")
    print(f"  {sorted(df[col].unique())}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 1: Regresion Lineal
# MAGIC
# MAGIC Empezamos con el modelo mas simple e interpretable.
# MAGIC Los coeficientes nos dicen cuantos puntos sube o baja cada variable.
# MAGIC
# MAGIC > Con el dataframe `df` que ya esta cargado, haz lo siguiente:
# MAGIC >
# MAGIC > 1. Crea nuevas columnas numericas (usa los valores exactos que
# MAGIC >    aparecen en la celda anterior):
# MAGIC >    - `estrato`: extraer el numero de `fami_estratovivienda` (1 a 6, Sin Estrato=0)
# MAGIC >    - `edu_madre`: codificar `fami_educacionmadre` de 0 (Ninguno) a 9 (Postgrado)
# MAGIC >    - `edu_padre`: igual con `fami_educacionpadre`
# MAGIC >    - `oficial`: 1 si `cole_naturaleza` == "OFICIAL", 0 si no
# MAGIC >    - `rural`: 1 si `cole_area_ubicacion` == "RURAL", 0 si no
# MAGIC >    - `bilingue`: 1 si `cole_bilingue` == "S", 0 si no
# MAGIC >    - `hombre`: 1 si `estu_genero` == "M", 0 si no
# MAGIC >    - `internet`: 1 si `fami_tieneinternet` == "Si", 0 si no
# MAGIC >    - `computador`: 1 si `fami_tienecomputador` == "Si", 0 si no
# MAGIC >    - `automovil`: 1 si `fami_tieneautomovil` == "Si", 0 si no
# MAGIC >    - `lavadora`: 1 si `fami_tienelavadora` == "Si", 0 si no
# MAGIC >
# MAGIC > 2. Aplica `.fillna(0)` a todas las columnas nuevas
# MAGIC >
# MAGIC > 3. Define X = df[columnas nuevas] (las 11 que creaste)
# MAGIC >    Define y = df["punt_global"] (esta es la variable a predecir)
# MAGIC >
# MAGIC > 4. Divide en train/test 80/20 con random_state=42
# MAGIC >
# MAGIC > 5. Entrena una LinearRegression de sklearn, imprime MAE y R2
# MAGIC >
# MAGIC > 6. Grafica barras horizontales con los coeficientes del modelo
# MAGIC >    mostrando cuantos puntos aporta cada variable

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 2: Gradient Boosting + comparacion
# MAGIC
# MAGIC Ahora un modelo mas poderoso. Y comparamos visualmente.
# MAGIC
# MAGIC > Con los mismos X_train, y_train, X_test, y_test de la celda anterior:
# MAGIC >
# MAGIC > 1. Entrena un GradientBoostingRegressor de sklearn con
# MAGIC >    n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42
# MAGIC >
# MAGIC > 2. Evalua con MAE y R2 sobre el test set
# MAGIC >
# MAGIC > 3. Crea una grafica de barras agrupadas comparando los dos modelos
# MAGIC >    (Regresion Lineal vs Gradient Boosting) mostrando MAE y R2
# MAGIC >    lado a lado. Indica cual modelo gano.
# MAGIC >
# MAGIC > 4. Guarda el mejor modelo en MLflow usando mlflow.autolog()
# MAGIC >    o mlflow.sklearn.log_model()

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ## Prompt 3: Que variables importan + prediccion en vivo
# MAGIC
# MAGIC El momento revelador.
# MAGIC
# MAGIC > Con el modelo Gradient Boosting que acabas de entrenar:
# MAGIC >
# MAGIC > 1. Crea una grafica de barras horizontales con la importancia
# MAGIC >    de cada variable (feature_importances_), ordenada de mayor
# MAGIC >    a menor, con colores de rojo a verde
# MAGIC >
# MAGIC > 2. Crea un DataFrame con dos filas para predecir. Usa las mismas
# MAGIC >    columnas que tiene X_train:
# MAGIC >    - Estudiante A: estrato=1, edu_madre=1, edu_padre=1,
# MAGIC >      oficial=1, rural=1, bilingue=0, hombre=0,
# MAGIC >      internet=0, computador=0, automovil=0, lavadora=0
# MAGIC >    - Estudiante B: estrato=5, edu_madre=9, edu_padre=8,
# MAGIC >      oficial=0, rural=0, bilingue=1, hombre=1,
# MAGIC >      internet=1, computador=1, automovil=1, lavadora=1
# MAGIC >
# MAGIC > 3. Predice con el modelo y muestra:
# MAGIC >    "Perfil A: X puntos | Perfil B: X puntos | Diferencia: X puntos"

# COMMAND ----------


