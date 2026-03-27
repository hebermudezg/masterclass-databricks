# Databricks notebook source

# MAGIC %md
# MAGIC # 📊 Crear SQL Dashboard (Lakeview) - Cafe Origen
# MAGIC
# MAGIC **Requiere:** Databricks con plan Premium (trial incluido)
# MAGIC
# MAGIC En este notebook vamos a:
# MAGIC 1. Guardar los datos como tablas permanentes en Unity Catalog
# MAGIC 2. Crear las consultas SQL para el dashboard
# MAGIC 3. Luego creamos el dashboard visualmente desde la interfaz
# MAGIC
# MAGIC ### Ventaja sobre un notebook:
# MAGIC - El dashboard tiene URL propia que puedes compartir
# MAGIC - Se actualiza automaticamente
# MAGIC - No necesita que alguien ejecute codigo
# MAGIC - Se ve profesional (como Power BI o Tableau)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 1: Crear tablas permanentes
# MAGIC
# MAGIC En Community Edition usamos vistas temporales. Ahora vamos a crear tablas reales
# MAGIC que persisten y que el SQL Dashboard puede consumir.

# COMMAND ----------

# Leer los CSVs
df_ventas = (spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/ventas.csv"))

df_productos = (spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/productos.csv"))

df_sucursales = (spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", "true")
    .load("/FileStore/tables/sucursales.csv"))

# COMMAND ----------

# Crear schema (base de datos) para nuestro caso
spark.sql("CREATE SCHEMA IF NOT EXISTS cafe_origen")

# COMMAND ----------

# Guardar como tablas permanentes
df_ventas.write.mode("overwrite").saveAsTable("cafe_origen.ventas")
df_productos.write.mode("overwrite").saveAsTable("cafe_origen.productos")
df_sucursales.write.mode("overwrite").saveAsTable("cafe_origen.sucursales")

print("Tablas creadas en cafe_origen:")
spark.sql("SHOW TABLES IN cafe_origen").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 2: Crear vista enriquecida (join de todo)
# MAGIC
# MAGIC Esta vista combina ventas + productos + sucursales. Es la base del dashboard.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW cafe_origen.ventas_completas AS
# MAGIC SELECT
# MAGIC     v.venta_id,
# MAGIC     v.fecha,
# MAGIC     v.hora,
# MAGIC     CAST(SUBSTRING(v.hora, 1, 2) AS INT) as hora_dia,
# MAGIC     DAYOFWEEK(v.fecha) as dia_semana_num,
# MAGIC     CASE DAYOFWEEK(v.fecha)
# MAGIC         WHEN 1 THEN 'Domingo'
# MAGIC         WHEN 2 THEN 'Lunes'
# MAGIC         WHEN 3 THEN 'Martes'
# MAGIC         WHEN 4 THEN 'Miercoles'
# MAGIC         WHEN 5 THEN 'Jueves'
# MAGIC         WHEN 6 THEN 'Viernes'
# MAGIC         WHEN 7 THEN 'Sabado'
# MAGIC     END as dia_semana,
# MAGIC     DATE_FORMAT(v.fecha, 'yyyy-MM') as mes,
# MAGIC     v.cantidad,
# MAGIC     v.precio_unitario,
# MAGIC     v.descuento_pct,
# MAGIC     v.total,
# MAGIC     v.metodo_pago,
# MAGIC     CASE
# MAGIC         WHEN v.metodo_pago = 'efectivo' THEN 'Efectivo'
# MAGIC         WHEN v.metodo_pago IN ('nequi', 'daviplata') THEN 'Digital'
# MAGIC         ELSE 'Tarjeta'
# MAGIC     END as tipo_pago,
# MAGIC     p.nombre as producto,
# MAGIC     p.categoria,
# MAGIC     p.precio,
# MAGIC     p.costo,
# MAGIC     p.origen_cafe,
# MAGIC     (v.total - (v.cantidad * p.costo)) as ganancia,
# MAGIC     s.nombre as sucursal,
# MAGIC     s.ciudad,
# MAGIC     s.tipo as tipo_sucursal
# MAGIC FROM cafe_origen.ventas v
# MAGIC JOIN cafe_origen.productos p ON v.producto_id = p.producto_id
# MAGIC JOIN cafe_origen.sucursales s ON v.sucursal_id = s.sucursal_id

# COMMAND ----------

# Verificar la vista
display(spark.sql("SELECT * FROM cafe_origen.ventas_completas LIMIT 5"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) as total_registros FROM cafe_origen.ventas_completas

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 3: Consultas para el Dashboard
# MAGIC
# MAGIC Estas son las consultas que usaremos en cada widget del dashboard.
# MAGIC Copialas al crear el SQL Dashboard.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 1: KPIs principales

# COMMAND ----------

# MAGIC %sql
# MAGIC -- KPIs: copiar esta consulta al dashboard
# MAGIC SELECT
# MAGIC     COUNT(*) as total_transacciones,
# MAGIC     CONCAT('$', FORMAT_NUMBER(SUM(total), 0)) as ingresos_totales,
# MAGIC     CONCAT('$', FORMAT_NUMBER(AVG(total), 0)) as ticket_promedio,
# MAGIC     CONCAT('$', FORMAT_NUMBER(SUM(ganancia), 0)) as ganancia_total,
# MAGIC     CONCAT(ROUND(SUM(ganancia) / SUM(total) * 100, 1), '%') as margen
# MAGIC FROM cafe_origen.ventas_completas

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 2: Tendencia mensual

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Tendencia mensual: grafico de lineas
# MAGIC SELECT
# MAGIC     mes,
# MAGIC     SUM(total) as ingresos,
# MAGIC     COUNT(*) as transacciones
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY mes
# MAGIC ORDER BY mes

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 3: Ranking de sucursales

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Sucursales: grafico de barras horizontal
# MAGIC SELECT
# MAGIC     sucursal,
# MAGIC     ciudad,
# MAGIC     SUM(total) as ingresos,
# MAGIC     SUM(ganancia) as ganancia,
# MAGIC     COUNT(*) as transacciones
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY sucursal, ciudad
# MAGIC ORDER BY ingresos DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 4: Categorias (dona)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Categorias: grafico de dona/pie
# MAGIC SELECT
# MAGIC     categoria,
# MAGIC     SUM(total) as ingresos,
# MAGIC     ROUND(SUM(total) * 100.0 / (SELECT SUM(total) FROM cafe_origen.ventas_completas), 1) as porcentaje
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY categoria
# MAGIC ORDER BY ingresos DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 5: Top 10 productos

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top productos: barras horizontales
# MAGIC SELECT
# MAGIC     producto,
# MAGIC     categoria,
# MAGIC     SUM(cantidad) as unidades,
# MAGIC     SUM(total) as ingresos,
# MAGIC     SUM(ganancia) as ganancia
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY producto, categoria
# MAGIC ORDER BY unidades DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 6: Metodos de pago

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Metodos de pago: barras
# MAGIC SELECT
# MAGIC     tipo_pago,
# MAGIC     COUNT(*) as transacciones,
# MAGIC     SUM(total) as ingresos
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY tipo_pago
# MAGIC ORDER BY transacciones DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Widget 7: Mapa de calor dia/hora

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Heatmap: tabla pivote
# MAGIC SELECT
# MAGIC     dia_semana,
# MAGIC     hora_dia,
# MAGIC     COUNT(*) as ventas
# MAGIC FROM cafe_origen.ventas_completas
# MAGIC GROUP BY dia_semana, dia_semana_num, hora_dia
# MAGIC ORDER BY dia_semana_num, hora_dia

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 4: Crear el Dashboard en la interfaz
# MAGIC
# MAGIC Ahora sal de este notebook y sigue estos pasos:
# MAGIC
# MAGIC 1. En la barra izquierda, click en **"SQL"** o **"Dashboards"**
# MAGIC 2. Click en **"Create Dashboard"** (o **"+ New" → "Dashboard"**)
# MAGIC 3. Nombre: **"Cafe Origen - Inteligencia de Negocio"**
# MAGIC 4. Para cada widget:
# MAGIC    - Click en **"Add" → "Visualization"**
# MAGIC    - Pega la consulta SQL correspondiente (las de arriba)
# MAGIC    - Selecciona el tipo de grafico
# MAGIC    - Configura los ejes
# MAGIC 5. Arrastra y organiza los widgets como quieras
# MAGIC 6. Click en **"Share"** → obtener URL publica
# MAGIC
# MAGIC ### Tip: Lakeview Dashboard (nuevo)
# MAGIC Si ves la opcion "Lakeview", usala. Es la version nueva y mas bonita de los dashboards.
# MAGIC Solo necesitas seleccionar la tabla `cafe_origen.ventas_completas` y Databricks
# MAGIC sugiere visualizaciones automaticamente.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Paso 5: Configurar Genie
# MAGIC
# MAGIC Genie permite que cualquier persona haga preguntas en lenguaje natural sobre los datos.
# MAGIC
# MAGIC 1. En la barra izquierda, busca **"Genie"** (o **"AI/BI Genie"**)
# MAGIC 2. Click en **"New Genie Space"**
# MAGIC 3. Nombre: **"Cafe Origen Assistant"**
# MAGIC 4. Selecciona las tablas: `cafe_origen.ventas_completas`
# MAGIC 5. Agrega instrucciones (opcional):
# MAGIC    > "Estos son datos de ventas de una cadena de cafeterias colombiana llamada Cafe Origen.
# MAGIC    > Los montos estan en pesos colombianos (COP). Hay 5 sucursales en Bogota, Medellin,
# MAGIC    > Cali y Bucaramanga. Responde siempre en espanol."
# MAGIC 6. Guarda y prueba con preguntas como:
# MAGIC    - "Cual es la sucursal con mas ventas?"
# MAGIC    - "Que producto tiene el mejor margen?"
# MAGIC    - "Como se comparan las ventas de diciembre vs enero?"
# MAGIC    - "A que hora se vende mas cafe?"
