# Databricks notebook source

# MAGIC %md
# MAGIC # 🔍 Exploración de Datos (EDA) - Café Origen
# MAGIC
# MAGIC **Objetivo:** Entender la estructura y calidad de los datos antes de analizarlos.
# MAGIC
# MAGIC En este notebook usaremos el **Databricks Assistant** para generar código.
# MAGIC
# MAGIC ### ¿Cómo usar el Databricks Assistant?
# MAGIC 1. Haz click en una celda vacía
# MAGIC 2. Presiona el ícono de IA o escribe `/` para activar el asistente
# MAGIC 3. Describe en lenguaje natural lo que quieres hacer
# MAGIC 4. El asistente genera el código por ti

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 1: Cargar los datos
# MAGIC Primero ejecutemos el notebook de setup para tener los datos disponibles.

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 2: Estadísticas descriptivas
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:** Escribe en el asistente:
# MAGIC > "Muéstrame las estadísticas descriptivas del dataframe df_ventas"

# COMMAND ----------

# Estadísticas descriptivas de ventas
display(df_ventas.describe())

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 3: ¿Cuántas ventas hay por mes?
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:**
# MAGIC > "Agrupa las ventas por mes y cuenta cuántas hay en cada mes, ordena cronológicamente"

# COMMAND ----------

from pyspark.sql.functions import col, month, year, count, sum as spark_sum, avg, round as spark_round, concat_ws

# Ventas por mes
df_ventas_mes = (df_ventas
    .withColumn("anio", year("fecha"))
    .withColumn("mes", month("fecha"))
    .groupBy("anio", "mes")
    .agg(
        count("*").alias("num_ventas"),
        spark_round(spark_sum("total"), 0).alias("total_ventas"),
        spark_round(avg("total"), 0).alias("ticket_promedio")
    )
    .orderBy("anio", "mes")
)

display(df_ventas_mes)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 4: ¿Cuáles son los métodos de pago más usados?
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:**
# MAGIC > "Cuenta las ventas por método de pago y muéstralo como gráfico de barras"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     metodo_pago,
# MAGIC     COUNT(*) as cantidad,
# MAGIC     ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ventas), 1) as porcentaje
# MAGIC FROM ventas
# MAGIC GROUP BY metodo_pago
# MAGIC ORDER BY cantidad DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 5: ¿Hay valores nulos o datos faltantes?
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:**
# MAGIC > "Verifica si hay valores nulos en cada columna del dataframe de ventas"

# COMMAND ----------

from pyspark.sql.functions import when, isnan, isnull

# Contar nulos por columna
null_counts = df_ventas.select([
    count(when(isnull(c), c)).alias(c)
    for c in df_ventas.columns
])

display(null_counts)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 6: Distribución de ventas por hora del día
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:**
# MAGIC > "Extrae la hora de la columna 'hora' y cuenta las ventas por cada hora del día"

# COMMAND ----------

from pyspark.sql.functions import substring

df_por_hora = (df_ventas
    .withColumn("hora_dia", substring("hora", 1, 2).cast("int"))
    .groupBy("hora_dia")
    .agg(count("*").alias("num_ventas"))
    .orderBy("hora_dia")
)

display(df_por_hora)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 7: Top 5 productos más vendidos (por cantidad)
# MAGIC
# MAGIC 💡 **Prueba con el Assistant:**
# MAGIC > "Haz un join entre ventas y productos, agrupa por nombre de producto, suma las cantidades y muestra el top 5"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     p.nombre,
# MAGIC     p.categoria,
# MAGIC     SUM(v.cantidad) as unidades_vendidas,
# MAGIC     SUM(v.total) as ingresos_totales
# MAGIC FROM ventas v
# MAGIC JOIN productos p ON v.producto_id = p.producto_id
# MAGIC GROUP BY p.nombre, p.categoria
# MAGIC ORDER BY unidades_vendidas DESC
# MAGIC LIMIT 5

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Exploración completa
# MAGIC
# MAGIC **Hallazgos clave hasta ahora:**
# MAGIC - Sabemos cuántas ventas tenemos y su distribución temporal
# MAGIC - Identificamos los métodos de pago preferidos
# MAGIC - Conocemos las horas pico de venta
# MAGIC - Tenemos el top de productos
# MAGIC
# MAGIC Continúa con el notebook **02_transformaciones** para análisis más profundo.
