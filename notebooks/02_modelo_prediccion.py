# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a entrenar un modelo que prediga el puntaje del ICFES
# MAGIC usando **solo variables socioeconomicas** (estrato, educacion
# MAGIC de los padres, tipo de colegio, acceso a internet).
# MAGIC
# MAGIC Ninguna variable academica. Solo contexto.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 1: Cargar los datos de la tabla Delta

# COMMAND ----------

import pandas as pd
import numpy as np

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes cargados")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 2: Preparar las variables
# MAGIC
# MAGIC El modelo necesita numeros, no texto. Convertimos:
# MAGIC - Estrato 1 a 6 → numeros del 1 al 6
# MAGIC - Educacion de los padres → escala del 0 (ninguno) al 9 (postgrado)
# MAGIC - Si/No (internet, computador, etc.) → 1/0
# MAGIC - Oficial/Privado → 1/0

# COMMAND ----------

# Codificacion ordinal: a mayor valor, mayor nivel
df["estrato_cod"] = df["fami_estratovivienda"].map(
    {"Sin Estrato": 0, "Estrato 1": 1, "Estrato 2": 2, "Estrato 3": 3,
     "Estrato 4": 4, "Estrato 5": 5, "Estrato 6": 6}
).fillna(0).astype(int)

MAPA_EDU = {
    "Ninguno": 0, "Primaria incompleta": 1, "Primaria completa": 2,
    "Secundaria (Bachillerato) incompleta": 3, "Secundaria (Bachillerato) completa": 4,
    u"T\u00e9cnica o tecnol\u00f3gica incompleta": 5, u"T\u00e9cnica o tecnol\u00f3gica completa": 6,
    u"Educaci\u00f3n profesional incompleta": 7, u"Educaci\u00f3n profesional completa": 8,
    "Postgrado": 9,
}
df["edu_madre_cod"] = df["fami_educacionmadre"].map(MAPA_EDU).fillna(0).astype(int)
df["edu_padre_cod"] = df["fami_educacionpadre"].map(MAPA_EDU).fillna(0).astype(int)

# COMMAND ----------

# Variables binarias: Si = 1, No = 0
df["colegio_oficial"] = (df["cole_naturaleza"] == "OFICIAL").astype(int)
df["colegio_rural"] = (df["cole_area_ubicacion"] == "RURAL").astype(int)
df["colegio_bilingue"] = (df["cole_bilingue"] == "S").astype(int)
df["genero_m"] = (df["estu_genero"] == "M").astype(int)
df["tiene_internet"] = (df["fami_tieneinternet"] == "Si").astype(int)
df["tiene_computador"] = (df["fami_tienecomputador"] == "Si").astype(int)
df["tiene_automovil"] = (df["fami_tieneautomovil"] == "Si").astype(int)
df["tiene_lavadora"] = (df["fami_tienelavadora"] == "Si").astype(int)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 3: Definir las 12 variables del modelo
# MAGIC
# MAGIC Estas son las unicas variables que le damos al modelo.
# MAGIC Ninguna es un puntaje academico. Solo contexto socioeconomico.

# COMMAND ----------

FEATURES = [
    "estrato_cod", "edu_madre_cod", "edu_padre_cod",
    "colegio_oficial", "colegio_rural", "colegio_bilingue",
    "genero_m", "tiene_internet", "tiene_computador",
    "tiene_automovil", "tiene_lavadora",
]

X = df[FEATURES]
y = df["punt_global"].dropna()
X = X.loc[y.index]

print(f"{len(FEATURES)} variables -> predecir punt_global")
print(f"{len(X):,} estudiantes listos para entrenar")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 4: Entrenar el modelo
# MAGIC
# MAGIC Usamos **Random Forest**: un algoritmo que consulta a 200
# MAGIC arboles de decision y promedia sus respuestas.
# MAGIC
# MAGIC **MLflow** registra automaticamente todo el experimento
# MAGIC (parametros, metricas, modelo) para que sea reproducible.

# COMMAND ----------

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import mlflow

mlflow.set_registry_uri("databricks-uc")
mlflow.autolog()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 5: Que tan bueno es?

# COMMAND ----------

y_pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Error promedio: {mae:.0f} puntos")
print(f"R2: {r2:.3f} ({r2*100:.0f}% de la variacion explicada)")
print(f"\nSolo con contexto socioeconomico, el modelo explica el {r2*100:.0f}% del puntaje")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 6: Que variables importan mas?
# MAGIC
# MAGIC Este es el hallazgo mas revelador. El modelo nos dice
# MAGIC que factores pesan mas al predecir el puntaje.

# COMMAND ----------

import matplotlib.pyplot as plt

nombres = {
    "estrato_cod": "Estrato", "edu_madre_cod": "Edu. Madre",
    "edu_padre_cod": "Edu. Padre", "colegio_oficial": "Oficial",
    "colegio_rural": "Rural", "colegio_bilingue": "Bilingue",
    "genero_m": "Genero", "tiene_internet": "Internet",
    "tiene_computador": "Computador", "tiene_automovil": "Automovil",
    "tiene_lavadora": "Lavadora",
}

imp = pd.Series(modelo.feature_importances_, index=[nombres[f] for f in FEATURES]).sort_values()
imp.plot(kind="barh", figsize=(10, 6), color=plt.cm.RdYlGn(np.linspace(0.15, 0.95, len(imp))))
plt.title("Que determina tu puntaje del ICFES?", fontsize=15, fontweight="bold")
plt.xlabel("Importancia")
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 7: Probemos con dos perfiles contrastantes

# COMMAND ----------

perfil_a = pd.DataFrame([{
    "estrato_cod": 1, "edu_madre_cod": 1, "edu_padre_cod": 1,
    "colegio_oficial": 1, "colegio_rural": 1, "colegio_bilingue": 0,
    "genero_m": 0, "tiene_internet": 0, "tiene_computador": 0,
    "tiene_automovil": 0, "tiene_lavadora": 0,
}])

perfil_b = pd.DataFrame([{
    "estrato_cod": 5, "edu_madre_cod": 9, "edu_padre_cod": 8,
    "colegio_oficial": 0, "colegio_rural": 0, "colegio_bilingue": 1,
    "genero_m": 1, "tiene_internet": 1, "tiene_computador": 1,
    "tiene_automovil": 1, "tiene_lavadora": 1,
}])

pred_a = modelo.predict(perfil_a)[0]
pred_b = modelo.predict(perfil_b)[0]

print("PERFIL A: Estrato 1, oficial rural, mama primaria, sin internet")
print(f"  -> {pred_a:.0f} puntos")
print()
print("PERFIL B: Estrato 5, privado bilingue, mama postgrado, con internet")
print(f"  -> {pred_b:.0f} puntos")
print()
print(f"Diferencia: {pred_b - pred_a:.0f} puntos")
