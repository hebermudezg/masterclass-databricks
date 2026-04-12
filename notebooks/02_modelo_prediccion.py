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

# Estructura de las columnas que vamos a usar como features
for col in ["fami_estratovivienda", "fami_educacionmadre", "fami_educacionpadre",
            "cole_naturaleza", "cole_area_ubicacion", "cole_bilingue",
            "estu_genero", "fami_tieneinternet", "fami_tienecomputador",
            "fami_tieneautomovil", "fami_tienelavadora"]:
    vals = sorted(df[col].unique())
    print(f"{col} ({len(vals)} valores): {vals}")

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 1: Preparar datos y entrenar Regresion Lineal
# MAGIC
# MAGIC > Tengo el dataframe `df` con resultados del ICFES Saber 11.
# MAGIC > Quiero predecir `punt_global` usando estas columnas como features:
# MAGIC > `fami_estratovivienda`, `fami_educacionmadre`, `fami_educacionpadre`,
# MAGIC > `cole_naturaleza`, `cole_area_ubicacion`, `cole_bilingue`,
# MAGIC > `estu_genero`, `fami_tieneinternet`, `fami_tienecomputador`,
# MAGIC > `fami_tieneautomovil`, `fami_tienelavadora`.
# MAGIC >
# MAGIC > Usa sklearn.preprocessing para transformar las variables:
# MAGIC > - OrdinalEncoder para las columnas ordinales (estrato y niveles
# MAGIC >   de educacion), respetando el orden natural de menor a mayor.
# MAGIC > - Las columnas binarias (Si/No, OFICIAL/NO OFICIAL, URBANO/RURAL,
# MAGIC >   S/N, M/F) codificalas como 0/1.
# MAGIC > - Usa ColumnTransformer para aplicar las transformaciones.
# MAGIC > - Maneja valores desconocidos con handle_unknown="use_encoded_value",
# MAGIC >   unknown_value=-1.
# MAGIC >
# MAGIC > Divide 80/20 con random_state=42.
# MAGIC > Entrena una LinearRegression con Pipeline (transformer + modelo).
# MAGIC > Imprime MAE y R2.
# MAGIC > Grafica barras horizontales con los coeficientes del modelo
# MAGIC > mostrando cuantos puntos aporta cada variable. Pon el valor
# MAGIC > numerico al lado de cada barra.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 2: Entrenar Gradient Boosting, comparar y guardar
# MAGIC
# MAGIC > Con los mismos datos transformados (X_train, X_test, y_train, y_test)
# MAGIC > o el mismo ColumnTransformer del paso anterior:
# MAGIC >
# MAGIC > Entrena un GradientBoostingRegressor(n_estimators=200, max_depth=5,
# MAGIC > learning_rate=0.1, random_state=42). Imprime MAE y R2.

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ## Prompt 3: Comparar modelos, importancia de variables y prediccion
# MAGIC
# MAGIC > Con los dos modelos entrenados (Regresion Lineal y Gradient Boosting):
# MAGIC >
# MAGIC > 1. Crea una figura con 2 subplots comparando ambos modelos:
# MAGIC >    subplot 1 con MAE, subplot 2 con R2. Colores distintos,
# MAGIC >    valores encima de las barras. Indica cual modelo es mejor.
# MAGIC >
# MAGIC > 2. Con el mejor modelo, grafica la importancia de cada variable
# MAGIC >    como barras horizontales ordenadas de mayor a menor.
# MAGIC >    Titulo: "Que determina tu puntaje del ICFES?"
# MAGIC >
# MAGIC > 3. Predice para dos estudiantes creando un DataFrame con las
# MAGIC > columnas originales (ANTES de transformar) y pasandolo por el
# MAGIC > pipeline o transformer:
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
# MAGIC > Guarda el modelo Gradient Boosting en MLflow junto con sus
# MAGIC > metricas (MAE y R2) para poder cargarlo y reutilizarlo despues.
# MAGIC > Antes de guardar usa mlflow.set_registry_uri("databricks")
# MAGIC > para evitar errores con Unity Catalog.
# MAGIC > Imprime el run_id.
# MAGIC > Solo guardar el modelo como artefacto del run.

# COMMAND ----------


