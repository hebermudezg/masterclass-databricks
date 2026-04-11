# Databricks notebook source
# MAGIC %md
# MAGIC # Modelo de Prediccion: Puntaje ICFES
# MAGIC
# MAGIC Vamos a entrenar un modelo que prediga el puntaje del ICFES
# MAGIC usando **solo variables socioeconomicas**.
# MAGIC
# MAGIC Ninguna variable academica. Solo contexto.
# MAGIC
# MAGIC Para cada paso, le pedimos al asistente de IA que nos ayude
# MAGIC a escribir el codigo.

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Carga los datos de la tabla Delta `icfes_saber11`

# COMMAND ----------

import pandas as pd, numpy as np

df = spark.table("default.icfes_saber11").toPandas()
print(f"{df.shape[0]:,} estudiantes")

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Convierte las columnas categoricas a numeros.
# MAGIC > Estrato de 1 a 6, educacion de 0 (ninguno) a 9 (postgrado),
# MAGIC > y las columnas Si/No a 1/0.

# COMMAND ----------

df["estrato"] = df["fami_estratovivienda"].map(
    {"Sin Estrato":0,"Estrato 1":1,"Estrato 2":2,"Estrato 3":3,
     "Estrato 4":4,"Estrato 5":5,"Estrato 6":6}).fillna(0).astype(int)

edu = {"Ninguno":0,"Primaria incompleta":1,"Primaria completa":2,
       "Secundaria (Bachillerato) incompleta":3,"Secundaria (Bachillerato) completa":4,
       "T\u00e9cnica o tecnol\u00f3gica incompleta":5,"T\u00e9cnica o tecnol\u00f3gica completa":6,
       "Educaci\u00f3n profesional incompleta":7,"Educaci\u00f3n profesional completa":8,
       "Postgrado":9}
df["edu_madre"] = df["fami_educacionmadre"].map(edu).fillna(0).astype(int)
df["edu_padre"] = df["fami_educacionpadre"].map(edu).fillna(0).astype(int)

for col, val in [("oficial","OFICIAL"),("rural","RURAL"),("bilingue","S"),
                 ("hombre","M"),("internet","Si"),("computador","Si"),
                 ("automovil","Si"),("lavadora","Si")]:
    src = {"oficial":"cole_naturaleza","rural":"cole_area_ubicacion",
           "bilingue":"cole_bilingue","hombre":"estu_genero",
           "internet":"fami_tieneinternet","computador":"fami_tienecomputador",
           "automovil":"fami_tieneautomovil","lavadora":"fami_tienelavadora"}[col]
    df[col] = (df[src] == val).astype(int)

print("Variables listas")

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Entrena un Random Forest para predecir `punt_global`
# MAGIC > usando solo estas variables socioeconomicas. Registra el
# MAGIC > experimento con MLflow.

# COMMAND ----------

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import mlflow

features = ["estrato","edu_madre","edu_padre","oficial","rural",
            "bilingue","hombre","internet","computador","automovil","lavadora"]

X = df[features]
y = df["punt_global"].dropna()
X = X.loc[y.index]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_registry_uri("databricks-uc")
mlflow.autolog()
modelo = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
modelo.fit(X_train, y_train)

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Que tan preciso es el modelo?

# COMMAND ----------

y_pred = modelo.predict(X_test)
print(f"Error promedio: {mean_absolute_error(y_test, y_pred):.0f} puntos")
print(f"R2: {r2_score(y_test, y_pred):.3f} ({r2_score(y_test, y_pred)*100:.0f}% de variacion explicada)")

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Muestra una grafica de que variables son las mas
# MAGIC > importantes para predecir el puntaje.

# COMMAND ----------

import matplotlib.pyplot as plt

nombres = {"estrato":"Estrato","edu_madre":"Edu. Madre","edu_padre":"Edu. Padre",
           "oficial":"Oficial","rural":"Rural","bilingue":"Bilingue","hombre":"Genero",
           "internet":"Internet","computador":"Computador","automovil":"Automovil",
           "lavadora":"Lavadora"}

imp = pd.Series(modelo.feature_importances_, index=[nombres[f] for f in features]).sort_values()
imp.plot(kind="barh", figsize=(10,6), color=plt.cm.RdYlGn(np.linspace(0.15,0.95,len(imp))))
plt.title("Que determina tu puntaje del ICFES?", fontsize=15, fontweight="bold")
plt.xlabel("Importancia")
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC > **Solicitud:** Predice el puntaje para dos estudiantes con
# MAGIC > perfiles contrastantes y muestra la diferencia.

# COMMAND ----------

a = modelo.predict(pd.DataFrame([dict(estrato=1,edu_madre=1,edu_padre=1,oficial=1,rural=1,bilingue=0,hombre=0,internet=0,computador=0,automovil=0,lavadora=0)]))[0]
b = modelo.predict(pd.DataFrame([dict(estrato=5,edu_madre=9,edu_padre=8,oficial=0,rural=0,bilingue=1,hombre=1,internet=1,computador=1,automovil=1,lavadora=1)]))[0]

print(f"Perfil A: Estrato 1, oficial rural, sin internet  ->  {a:.0f} puntos")
print(f"Perfil B: Estrato 5, privado bilingue, con internet  ->  {b:.0f} puntos")
print(f"\nDiferencia: {b-a:.0f} puntos")
