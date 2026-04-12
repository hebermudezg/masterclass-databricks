# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a entrenar modelos de machine learning para predecir el
# MAGIC puntaje del ICFES usando **solo variables socioeconomicas**.
# MAGIC
# MAGIC Le pedimos al asistente de IA que nos escriba el codigo.

# COMMAND ----------

import pandas as pd

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes, {df.shape[1]} columnas")
df.head()

# COMMAND ----------

# Valores reales de las columnas categoricas (para que el Assistant los vea)
for col in ["fami_estratovivienda", "fami_educacionmadre", "fami_educacionpadre",
            "cole_naturaleza", "cole_area_ubicacion", "cole_bilingue",
            "estu_genero", "fami_tieneinternet"]:
    print(f"\n{col}:")
    print(f"  {sorted(df[col].unique())}")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 1: Preparar datos y entrenar Regresion Lineal
# MAGIC
# MAGIC > Tengo el dataframe `df` con resultados del ICFES. Necesito predecir
# MAGIC > la columna `punt_global` usando variables socioeconomicas.
# MAGIC >
# MAGIC > Paso 1 - Crear columnas numericas usando los valores exactos que
# MAGIC > aparecen arriba en los unique():
# MAGIC > - `estrato`: de `fami_estratovivienda`, mapear "Estrato 1"=1, "Estrato 2"=2,
# MAGIC >   ..., "Estrato 6"=6, "Sin Estrato"=0. Aplicar fillna(0).
# MAGIC > - `edu_madre`: de `fami_educacionmadre`, mapear en orden de menor a mayor
# MAGIC >   nivel educativo (0=Ninguno, 9=Postgrado). Usar los strings exactos
# MAGIC >   del unique(). Aplicar fillna(0).
# MAGIC > - `edu_padre`: igual que edu_madre pero con `fami_educacionpadre`.
# MAGIC > - `oficial`: 1 si `cole_naturaleza`=="OFICIAL", else 0
# MAGIC > - `rural`: 1 si `cole_area_ubicacion`=="RURAL", else 0
# MAGIC > - `bilingue`: 1 si `cole_bilingue`=="S", else 0
# MAGIC > - `hombre`: 1 si `estu_genero`=="M", else 0
# MAGIC > - `internet`: 1 si `fami_tieneinternet`=="Si", else 0
# MAGIC > - `computador`: 1 si `fami_tienecomputador`=="Si", else 0
# MAGIC > - `automovil`: 1 si `fami_tieneautomovil`=="Si", else 0
# MAGIC > - `lavadora`: 1 si `fami_tienelavadora`=="Si", else 0
# MAGIC >
# MAGIC > Paso 2 - Definir X con esas 11 columnas y y = punt_global.
# MAGIC > Dividir 80/20 con random_state=42.
# MAGIC >
# MAGIC > Paso 3 - Entrenar LinearRegression de sklearn. Imprimir MAE y R2.
# MAGIC >
# MAGIC > Paso 4 - Graficar barras horizontales con los coeficientes del modelo
# MAGIC > (cuantos puntos suma o resta cada variable). Titulo: "Cuantos puntos
# MAGIC > aporta cada variable al puntaje del ICFES?"

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Entrenar Gradient Boosting y comparar ambos modelos
# MAGIC
# MAGIC > Con los mismos X_train, y_train, X_test, y_test que ya existen:
# MAGIC >
# MAGIC > Paso 1 - Entrenar un GradientBoostingRegressor de sklearn con
# MAGIC > n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42.
# MAGIC > Imprimir MAE y R2.
# MAGIC >
# MAGIC > Paso 2 - Crear una grafica con dos subplots lado a lado:
# MAGIC > - Subplot 1: barras comparando el MAE de ambos modelos
# MAGIC > - Subplot 2: barras comparando el R2 de ambos modelos
# MAGIC > Usar colores diferentes para cada modelo. Poner etiquetas con los
# MAGIC > valores encima de cada barra. Titulo: "Regresion Lineal vs Gradient Boosting"

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 3: Variables mas importantes y prediccion de perfiles
# MAGIC
# MAGIC > Con el modelo Gradient Boosting:
# MAGIC >
# MAGIC > Paso 1 - Graficar barras horizontales con feature_importances_,
# MAGIC > ordenadas de mayor a menor. Usar colormap RdYlGn (rojo=menos,
# MAGIC > verde=mas). Titulo: "Que determina tu puntaje del ICFES?"
# MAGIC >
# MAGIC > Paso 2 - Predecir el puntaje para dos estudiantes. Crear un
# MAGIC > DataFrame con las mismas columnas de X_train:
# MAGIC > - Estudiante A: estrato=1, edu_madre=1, edu_padre=1, oficial=1,
# MAGIC >   rural=1, bilingue=0, hombre=0, internet=0, computador=0,
# MAGIC >   automovil=0, lavadora=0
# MAGIC > - Estudiante B: estrato=5, edu_madre=9, edu_padre=8, oficial=0,
# MAGIC >   rural=0, bilingue=1, hombre=1, internet=1, computador=1,
# MAGIC >   automovil=1, lavadora=1
# MAGIC >
# MAGIC > Imprimir:
# MAGIC > "Perfil A (E1, oficial rural, sin internet): XXX puntos"
# MAGIC > "Perfil B (E5, privado bilingue, con internet): XXX puntos"
# MAGIC > "Diferencia: XXX puntos"

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 4: Guardar el mejor modelo en MLflow
# MAGIC
# MAGIC > Guarda el modelo Gradient Boosting en MLflow:
# MAGIC >
# MAGIC > 1. Usa mlflow.set_experiment("/masterclass-icfes")
# MAGIC > 2. Inicia un run con mlflow.start_run(run_name="gradient_boosting_icfes")
# MAGIC > 3. Registra las metricas MAE y R2 con mlflow.log_metric()
# MAGIC > 4. Guarda el modelo con mlflow.sklearn.log_model(modelo_gb, "modelo")
# MAGIC > 5. Imprime el run_id
# MAGIC > 6. Cierra el run
# MAGIC >
# MAGIC > Luego intenta registrar el modelo con:
# MAGIC > mlflow.register_model(f"runs:/{run_id}/modelo", "prediccion_icfes")
# MAGIC > Si falla, imprime "Modelo guardado en Experiments (registro no disponible en Free Edition)"

# COMMAND ----------


