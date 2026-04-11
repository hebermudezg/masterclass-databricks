# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES Saber 11
# MAGIC
# MAGIC Entrenamos un modelo de ML para predecir el puntaje global del ICFES
# MAGIC usando SOLO variables socioeconomicas (estrato, educacion de los padres,
# MAGIC tipo de colegio, acceso a internet).
# MAGIC
# MAGIC **La pregunta provocadora:** Tu puntaje ya esta determinado antes de
# MAGIC sentarte a presentar el examen?

# COMMAND ----------

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import matplotlib.pyplot as plt

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Cargar datos limpios

# COMMAND ----------

df = spark.table("default.icfes_saber11").toPandas()
print(f"Datos cargados: {df.shape[0]:,} filas x {df.shape[1]} columnas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Ingenieria de features
# MAGIC
# MAGIC Convertimos variables categoricas a numeros.
# MAGIC Solo usamos variables que se conocen ANTES del examen (no los puntajes por materia).

# COMMAND ----------

# --- Estrato socioeconomico ---
MAPA_ESTRATO = {
    "Sin Estrato": 0, "Estrato 1": 1, "Estrato 2": 2, "Estrato 3": 3,
    "Estrato 4": 4, "Estrato 5": 5, "Estrato 6": 6,
}

# --- Educacion de los padres ---
MAPA_EDUCACION = {
    "Ninguno": 0,
    "Primaria incompleta": 1, "Primaria completa": 2,
    "Secundaria (Bachillerato) incompleta": 3,
    "Secundaria (Bachillerato) completa": 4,
    "Técnica o tecnológica incompleta": 5,
    "Técnica o tecnológica completa": 6,
    "Educación profesional incompleta": 7,
    "Educación profesional completa": 8,
    "Postgrado": 9,
}

# --- Personas en el hogar ---
MAPA_PERSONAS = {
    "1 a 2": 1, "3 a 4": 2, "5 a 6": 3, "7 a 8": 4, "9 o más": 5,
}

# Aplicar codificaciones
df["estrato_cod"] = df["fami_estratovivienda"].map(MAPA_ESTRATO).fillna(0).astype(int)
df["edu_madre_cod"] = df["fami_educacionmadre"].map(MAPA_EDUCACION).fillna(0).astype(int)
df["edu_padre_cod"] = df["fami_educacionpadre"].map(MAPA_EDUCACION).fillna(0).astype(int)
df["personas_hogar_cod"] = df["fami_personashogar"].map(MAPA_PERSONAS).fillna(2).astype(int)

# Variables binarias
df["colegio_oficial"] = (df["cole_naturaleza"] == "OFICIAL").astype(int)
df["colegio_rural"] = (df["cole_area_ubicacion"] == "RURAL").astype(int)
df["colegio_bilingue"] = (df["cole_bilingue"] == "S").astype(int)
df["genero_m"] = (df["estu_genero"] == "M").astype(int)
df["tiene_internet"] = (df["fami_tieneinternet"] == "Si").astype(int)
df["tiene_computador"] = (df["fami_tienecomputador"] == "Si").astype(int)
df["tiene_automovil"] = (df["fami_tieneautomovil"] == "Si").astype(int)
df["tiene_lavadora"] = (df["fami_tienelavadora"] == "Si").astype(int)

# Features para el modelo (solo variables socioeconomicas, NO puntajes por materia)
FEATURES = [
    "estrato_cod", "edu_madre_cod", "edu_padre_cod",
    "colegio_oficial", "colegio_rural", "colegio_bilingue",
    "genero_m", "tiene_internet", "tiene_computador",
    "tiene_automovil", "tiene_lavadora", "personas_hogar_cod",
]

X = df[FEATURES]
y = df["punt_global"]

mask = y.notna() & (y > 0)
X = X[mask]
y = y[mask]

print(f"Features ({len(FEATURES)} variables socioeconomicas):")
for f in FEATURES:
    print(f"  - {f}")
print(f"\nDatos para modelar: {X.shape[0]:,} filas")
print(f"Variable objetivo: punt_global (puntaje del ICFES)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Entrenar modelo con MLflow

# COMMAND ----------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Entrenamiento: {X_train.shape[0]:,} filas")
print(f"Prueba: {X_test.shape[0]:,} filas")

# COMMAND ----------

mlflow.set_experiment("/masterclass-icfes")

with mlflow.start_run(run_name="random_forest_icfes") as run:

    params = {
        "n_estimators": 200,
        "max_depth": 15,
        "min_samples_split": 20,
        "min_samples_leaf": 10,
        "random_state": 42,
        "n_jobs": -1,
    }

    modelo = RandomForestRegressor(**params)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    mlflow.log_params(params)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    signature = infer_signature(X_train, y_pred)
    mlflow.sklearn.log_model(modelo, "modelo", signature=signature)

    run_id = run.info.run_id

    print(f"Modelo entrenado y registrado en MLflow")
    print(f"  Run ID: {run_id}")
    print(f"  MAE:  {mae:.1f} puntos (error promedio)")
    print(f"  RMSE: {rmse:.1f} puntos")
    print(f"  R2:   {r2:.4f} ({r2*100:.1f}% de varianza explicada)")
    print()
    print(f"  Interpretacion: el modelo se equivoca en promedio por {mae:.0f} puntos")
    print(f"  Solo con variables socioeconomicas explica el {r2*100:.0f}% del puntaje")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Que variables importan mas?

# COMMAND ----------

# Nombres legibles para las features
NOMBRES_FEATURES = {
    "estrato_cod": "Estrato",
    "edu_madre_cod": "Educacion Madre",
    "edu_padre_cod": "Educacion Padre",
    "colegio_oficial": "Colegio Oficial",
    "colegio_rural": "Colegio Rural",
    "colegio_bilingue": "Colegio Bilingue",
    "genero_m": "Genero (Masculino)",
    "tiene_internet": "Internet en Casa",
    "tiene_computador": "Computador en Casa",
    "tiene_automovil": "Automovil",
    "tiene_lavadora": "Lavadora",
    "personas_hogar_cod": "Personas en Hogar",
}

importancias = pd.Series(
    modelo.feature_importances_,
    index=[NOMBRES_FEATURES.get(f, f) for f in FEATURES],
).sort_values()

fig, ax = plt.subplots(figsize=(12, 7))
colores = plt.cm.RdYlGn(np.linspace(0.15, 0.95, len(importancias)))
importancias.plot(kind="barh", ax=ax, color=colores, edgecolor="white")
ax.set_title("Que determina tu puntaje del ICFES?", fontsize=16, fontweight="bold")
ax.set_xlabel("Importancia en el modelo", fontsize=12)
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Prediccion vs Realidad

# COMMAND ----------

fig, ax = plt.subplots(figsize=(10, 8))
idx = np.random.choice(len(y_test), min(3000, len(y_test)), replace=False)
real = y_test.iloc[idx]
pred = y_pred[idx]

ax.scatter(real, pred, alpha=0.2, s=8, color="#1565C0")
lim_min, lim_max = 100, 450
ax.plot([lim_min, lim_max], [lim_min, lim_max], "r--", linewidth=2, label="Prediccion perfecta")
ax.set_xlabel("Puntaje Real", fontsize=13)
ax.set_ylabel("Puntaje Predicho", fontsize=13)
ax.set_title("Prediccion vs Realidad", fontsize=15, fontweight="bold")
ax.set_xlim(lim_min, lim_max)
ax.set_ylim(lim_min, lim_max)
ax.legend(fontsize=12)
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Registrar modelo

# COMMAND ----------

modelo_registrado = mlflow.register_model(
    f"runs:/{run_id}/modelo",
    "prediccion_icfes_saber11"
)

print(f"Modelo registrado: {modelo_registrado.name}")
print(f"Version: {modelo_registrado.version}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Probemos en vivo: dos perfiles contrastantes

# COMMAND ----------

perfiles = pd.DataFrame([
    {  # Perfil A
        "estrato_cod": 1, "edu_madre_cod": 1, "edu_padre_cod": 1,
        "colegio_oficial": 1, "colegio_rural": 1, "colegio_bilingue": 0,
        "genero_m": 0, "tiene_internet": 0, "tiene_computador": 0,
        "tiene_automovil": 0, "tiene_lavadora": 0, "personas_hogar_cod": 3,
    },
    {  # Perfil B
        "estrato_cod": 5, "edu_madre_cod": 9, "edu_padre_cod": 8,
        "colegio_oficial": 0, "colegio_rural": 0, "colegio_bilingue": 1,
        "genero_m": 1, "tiene_internet": 1, "tiene_computador": 1,
        "tiene_automovil": 1, "tiene_lavadora": 1, "personas_hogar_cod": 2,
    },
])

predicciones = modelo.predict(perfiles)

print("PERFIL A: Estrato 1, colegio oficial rural, mama con primaria, sin internet")
print(f"  Puntaje predicho: {predicciones[0]:.0f}")
print()
print("PERFIL B: Estrato 5, colegio privado bilingue, mama con postgrado, con internet")
print(f"  Puntaje predicho: {predicciones[1]:.0f}")
print()
print(f"Diferencia: {predicciones[1] - predicciones[0]:.0f} puntos")
print()
print("Cambien los valores y vuelvan a ejecutar!")
print("estrato_cod: 1-6 | edu_madre_cod: 0-9 | colegio_oficial: 0/1")

# COMMAND ----------

# MAGIC %md
# MAGIC La diferencia en las predicciones refleja desigualdades reales
# MAGIC en el sistema educativo colombiano. Este modelo no determina
# MAGIC el destino de nadie, pero si revela patrones estructurales
# MAGIC que deberian informar politicas publicas.
