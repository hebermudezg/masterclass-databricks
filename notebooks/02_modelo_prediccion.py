# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Entrenamos modelos de ML para predecir el puntaje del ICFES
# MAGIC usando **solo variables socioeconomicas**.
# MAGIC
# MAGIC Le pedimos al asistente de IA que escriba el codigo.

# COMMAND ----------

import pandas as pd

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes, {df.shape[1]} columnas")
df.head()

# COMMAND ----------

# Valores reales de cada columna categorica
for col in ["fami_estratovivienda", "fami_educacionmadre", "fami_educacionpadre",
            "cole_naturaleza", "cole_area_ubicacion", "cole_bilingue",
            "estu_genero", "fami_tieneinternet", "fami_tienecomputador",
            "fami_tieneautomovil", "fami_tienelavadora"]:
    print(f"{col}: {sorted(df[col].unique())}")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 1: Preparar datos y entrenar Regresion Lineal
# MAGIC
# MAGIC > Tengo el dataframe `df` con resultados del ICFES Saber 11.
# MAGIC >
# MAGIC > 1. Crea columnas numericas a partir de las categoricas. Mira los
# MAGIC >    valores unicos impresos en la celda anterior y usa esos strings
# MAGIC >    exactos para los mapeos:
# MAGIC >    - `estrato`: de `fami_estratovivienda`. Mapear cada "Estrato X" al
# MAGIC >      numero X (1-6), "Sin Estrato"=0. fillna(0).
# MAGIC >    - `edu_madre`: de `fami_educacionmadre`. Mapear cada valor unico
# MAGIC >      en orden ascendente de nivel educativo, desde 0 (Ninguno) hasta
# MAGIC >      9 (Postgrado). Usa los strings EXACTOS del unique(). fillna(0).
# MAGIC >    - `edu_padre`: igual que edu_madre pero desde `fami_educacionpadre`.
# MAGIC >    - `oficial`: (`cole_naturaleza`=="OFICIAL").astype(int)
# MAGIC >    - `rural`: (`cole_area_ubicacion`=="RURAL").astype(int)
# MAGIC >    - `bilingue`: (`cole_bilingue`=="S").astype(int)
# MAGIC >    - `hombre`: (`estu_genero`=="M").astype(int)
# MAGIC >    - `internet`: (`fami_tieneinternet`=="Si").astype(int)
# MAGIC >    - `computador`: (`fami_tienecomputador`=="Si").astype(int)
# MAGIC >    - `automovil`: (`fami_tieneautomovil`=="Si").astype(int)
# MAGIC >    - `lavadora`: (`fami_tienelavadora`=="Si").astype(int)
# MAGIC >
# MAGIC > 2. X = df[["estrato","edu_madre","edu_padre","oficial","rural","bilingue",
# MAGIC >    "hombre","internet","computador","automovil","lavadora"]]
# MAGIC >    y = df["punt_global"]
# MAGIC >
# MAGIC > 3. train_test_split 80/20, random_state=42
# MAGIC >
# MAGIC > 4. Entrena LinearRegression. Imprime MAE y R2.
# MAGIC >
# MAGIC > 5. Grafica barras horizontales con los coeficientes, ordenados por
# MAGIC >    valor absoluto. Titulo: "Cuantos puntos aporta cada variable?"
# MAGIC >    Poner el valor numerico al lado de cada barra.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Entrenar Gradient Boosting, comparar, y guardar el mejor
# MAGIC
# MAGIC > Con X_train, y_train, X_test, y_test que ya existen:
# MAGIC >
# MAGIC > 1. Entrena GradientBoostingRegressor(n_estimators=200, max_depth=5,
# MAGIC >    learning_rate=0.1, random_state=42). Imprime MAE y R2.
# MAGIC >
# MAGIC > 2. Crea una figura con 2 subplots lado a lado comparando los dos
# MAGIC >    modelos (Regresion Lineal vs Gradient Boosting):
# MAGIC >    - Subplot izquierdo: barras con MAE de cada modelo
# MAGIC >    - Subplot derecho: barras con R2 de cada modelo
# MAGIC >    Colores distintos, valores encima de las barras, titulo general:
# MAGIC >    "Comparacion de Modelos". Indicar el ganador.
# MAGIC >
# MAGIC > 3. Guardar el Gradient Boosting en MLflow:
# MAGIC >    - import mlflow, mlflow.sklearn
# MAGIC >    - mlflow.set_experiment("/masterclass-icfes")
# MAGIC >    - Dentro de mlflow.start_run(run_name="mejor_modelo_icfes"):
# MAGIC >      - mlflow.log_metric("mae", mae del GB)
# MAGIC >      - mlflow.log_metric("r2", r2 del GB)
# MAGIC >      - mlflow.sklearn.log_model(modelo_gb, artifact_path="modelo",
# MAGIC >        registered_model_name="prediccion_icfes")
# MAGIC >    - Imprimir el run_id y "Modelo guardado como prediccion_icfes"

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 3: Variables mas importantes y prediccion en vivo
# MAGIC
# MAGIC > Con el modelo Gradient Boosting ya entrenado:
# MAGIC >
# MAGIC > 1. Grafica barras horizontales con feature_importances_ ordenadas
# MAGIC >    de mayor a menor. Usa colormap plt.cm.RdYlGn. Titulo:
# MAGIC >    "Que determina tu puntaje del ICFES?"
# MAGIC >    Poner el valor de importancia al lado de cada barra.
# MAGIC >
# MAGIC > 2. Predice para dos estudiantes. Crear DataFrame con las mismas
# MAGIC >    columnas de X_train (en el mismo orden):
# MAGIC >    Estudiante A: estrato=1, edu_madre=1, edu_padre=1, oficial=1,
# MAGIC >      rural=1, bilingue=0, hombre=0, internet=0, computador=0,
# MAGIC >      automovil=0, lavadora=0
# MAGIC >    Estudiante B: estrato=5, edu_madre=9, edu_padre=8, oficial=0,
# MAGIC >      rural=0, bilingue=1, hombre=1, internet=1, computador=1,
# MAGIC >      automovil=1, lavadora=1
# MAGIC >
# MAGIC > 3. Imprimir:
# MAGIC >    "Perfil A (E1, oficial rural, sin internet): XXX puntos"
# MAGIC >    "Perfil B (E5, privado bilingue, con internet): XXX puntos"
# MAGIC >    "Diferencia: XXX puntos"

# COMMAND ----------


