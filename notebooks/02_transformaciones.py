# Databricks notebook source

# MAGIC %md
# MAGIC # ⚙️ Transformaciones y Análisis - Café Origen
# MAGIC
# MAGIC **Objetivo:** Limpiar, transformar y cruzar datos para responder preguntas de negocio.
# MAGIC
# MAGIC ### Preguntas que vamos a responder:
# MAGIC 1. ¿Cuál es la sucursal más rentable?
# MAGIC 2. ¿Qué categoría de producto genera más ingresos?
# MAGIC 3. ¿Cómo se comportan las ventas entre semana vs fin de semana?
# MAGIC 4. ¿Cuál es el margen de ganancia por producto?

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análisis 1: Rentabilidad por Sucursal
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Haz un join entre ventas y sucursales, calcula el total de ingresos y número de transacciones por sucursal, ordena por ingresos de mayor a menor"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     s.nombre as sucursal,
# MAGIC     s.ciudad,
# MAGIC     s.tipo,
# MAGIC     COUNT(*) as num_transacciones,
# MAGIC     SUM(v.total) as ingresos_totales,
# MAGIC     ROUND(AVG(v.total), 0) as ticket_promedio,
# MAGIC     ROUND(SUM(v.total) / COUNT(DISTINCT v.fecha), 0) as ingreso_diario_promedio
# MAGIC FROM ventas v
# MAGIC JOIN sucursales s ON v.sucursal_id = s.sucursal_id
# MAGIC GROUP BY s.nombre, s.ciudad, s.tipo
# MAGIC ORDER BY ingresos_totales DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análisis 2: Ingresos por Categoría de Producto
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Calcula ingresos totales, cantidad vendida y margen de ganancia por categoría de producto"

# COMMAND ----------

from pyspark.sql.functions import col, sum as spark_sum, count, round as spark_round

df_categoria = (df_ventas
    .join(df_productos, "producto_id")
    .groupBy("categoria")
    .agg(
        spark_sum("total").alias("ingresos"),
        spark_sum("cantidad").alias("unidades"),
        spark_sum(col("cantidad") * col("costo")).alias("costo_total"),
        count("*").alias("transacciones")
    )
    .withColumn("ganancia", col("ingresos") - col("costo_total"))
    .withColumn("margen_pct", spark_round((col("ganancia") / col("ingresos")) * 100, 1))
    .orderBy(col("ingresos").desc())
)

display(df_categoria)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análisis 3: Semana vs Fin de Semana
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Agrega una columna que indique si la venta fue en día de semana o fin de semana, luego compara ventas promedio"

# COMMAND ----------

from pyspark.sql.functions import dayofweek, when

df_semana = (df_ventas
    .withColumn("dia_semana", dayofweek("fecha"))
    .withColumn("tipo_dia",
        when(col("dia_semana").isin(1, 7), "Fin de semana")
        .otherwise("Entre semana")
    )
    .groupBy("tipo_dia")
    .agg(
        count("*").alias("num_ventas"),
        spark_round(spark_sum("total"), 0).alias("ingresos_totales"),
        spark_round(avg("total"), 0).alias("ticket_promedio")
    )
)

from pyspark.sql.functions import avg

df_semana = (df_ventas
    .withColumn("dia_semana", dayofweek("fecha"))
    .withColumn("tipo_dia",
        when(col("dia_semana").isin(1, 7), "Fin de semana")
        .otherwise("Entre semana")
    )
    .groupBy("tipo_dia")
    .agg(
        count("*").alias("num_ventas"),
        spark_round(spark_sum("total"), 0).alias("ingresos_totales"),
        spark_round(avg("total"), 0).alias("ticket_promedio")
    )
)

display(df_semana)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análisis 4: Top 10 Productos por Margen de Ganancia
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Calcula el margen de ganancia por producto (ingreso - costo) y muestra los 10 con mayor margen total"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     p.nombre,
# MAGIC     p.categoria,
# MAGIC     p.precio,
# MAGIC     p.costo,
# MAGIC     p.precio - p.costo as margen_unitario,
# MAGIC     ROUND((p.precio - p.costo) * 100.0 / p.precio, 1) as margen_pct,
# MAGIC     SUM(v.cantidad) as unidades_vendidas,
# MAGIC     SUM(v.cantidad) * (p.precio - p.costo) as ganancia_total
# MAGIC FROM ventas v
# MAGIC JOIN productos p ON v.producto_id = p.producto_id
# MAGIC GROUP BY p.nombre, p.categoria, p.precio, p.costo
# MAGIC ORDER BY ganancia_total DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## Análisis 5: Tendencia mensual por sucursal
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Muestra la tendencia de ingresos mensuales por cada sucursal como gráfico de líneas"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     s.nombre as sucursal,
# MAGIC     DATE_FORMAT(v.fecha, 'yyyy-MM') as mes,
# MAGIC     SUM(v.total) as ingresos,
# MAGIC     COUNT(*) as transacciones
# MAGIC FROM ventas v
# MAGIC JOIN sucursales s ON v.sucursal_id = s.sucursal_id
# MAGIC GROUP BY s.nombre, DATE_FORMAT(v.fecha, 'yyyy-MM')
# MAGIC ORDER BY mes, sucursal

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Transformaciones completas
# MAGIC
# MAGIC **Insights obtenidos:**
# MAGIC - Ranking de sucursales por rentabilidad
# MAGIC - Categorías de producto más y menos rentables
# MAGIC - Diferencia de comportamiento semana vs fin de semana
# MAGIC - Productos estrella por margen de ganancia
# MAGIC - Tendencias mensuales por sucursal
# MAGIC
# MAGIC Continúa con el notebook **03_visualizacion** para el dashboard final.
