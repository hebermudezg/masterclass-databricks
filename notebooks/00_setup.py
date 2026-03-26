# Databricks notebook source

# MAGIC %md
# MAGIC # 🔧 Setup - Cargar Datos de Café Origen
# MAGIC
# MAGIC **Master Class: Análisis de Datos en Databricks con IA**
# MAGIC
# MAGIC En este notebook vamos a:
# MAGIC 1. Subir los archivos CSV al entorno de Databricks
# MAGIC 2. Crear DataFrames de Spark
# MAGIC 3. Verificar que los datos se cargaron correctamente

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 1: Subir los archivos CSV
# MAGIC
# MAGIC Antes de ejecutar este notebook, sube los 3 archivos CSV a Databricks:
# MAGIC 1. Ve a **Data** (barra lateral izquierda)
# MAGIC 2. Click en **Create Table**
# MAGIC 3. Arrastra los archivos: `ventas.csv`, `productos.csv`, `sucursales.csv`
# MAGIC 4. Los archivos quedarán en `/FileStore/tables/`
# MAGIC
# MAGIC **Alternativa rápida:** Usa el botón **Upload** en el explorador de archivos del workspace.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 2: Leer los archivos CSV como DataFrames

# COMMAND ----------

# Leer el archivo de ventas
df_ventas = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/ventas.csv")
)

print(f"Ventas cargadas: {df_ventas.count()} registros")
df_ventas.printSchema()

# COMMAND ----------

# Leer el archivo de productos
df_productos = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/productos.csv")
)

print(f"Productos cargados: {df_productos.count()} registros")
df_productos.printSchema()

# COMMAND ----------

# Leer el archivo de sucursales
df_sucursales = (spark.read
    .format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/sucursales.csv")
)

print(f"Sucursales cargadas: {df_sucursales.count()} registros")
df_sucursales.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 3: Vista previa de los datos

# COMMAND ----------

display(df_ventas.limit(10))

# COMMAND ----------

display(df_productos)

# COMMAND ----------

display(df_sucursales)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 4: Crear vistas temporales para usar SQL
# MAGIC
# MAGIC Esto nos permite consultar los datos con SQL desde cualquier notebook.

# COMMAND ----------

df_ventas.createOrReplaceTempView("ventas")
df_productos.createOrReplaceTempView("productos")
df_sucursales.createOrReplaceTempView("sucursales")

print("Vistas temporales creadas: ventas, productos, sucursales")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verificación rápida con SQL
# MAGIC SELECT 'ventas' as tabla, COUNT(*) as registros FROM ventas
# MAGIC UNION ALL
# MAGIC SELECT 'productos', COUNT(*) FROM productos
# MAGIC UNION ALL
# MAGIC SELECT 'sucursales', COUNT(*) FROM sucursales

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Setup completo
# MAGIC Los datos están listos. Continúa con el notebook **01_exploracion**.
