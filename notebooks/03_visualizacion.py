# Databricks notebook source

# MAGIC %md
# MAGIC # 📊 Visualización y Dashboard - Café Origen
# MAGIC
# MAGIC **Objetivo:** Crear un mini-dashboard con las visualizaciones más importantes para presentar a la gerencia de Café Origen.
# MAGIC
# MAGIC ### Tip importante sobre gráficos en Databricks:
# MAGIC Después de ejecutar una celda con `display()`, haz click en el ícono de **gráfico** (📊) debajo del resultado para cambiar el tipo de visualización: barras, líneas, pastel, mapa, etc.

# COMMAND ----------

# MAGIC %run ./00_setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📈 Gráfico 1: Ingresos Mensuales (Tendencia General)
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Crea un gráfico de líneas con los ingresos totales por mes"
# MAGIC
# MAGIC Después de ejecutar, selecciona visualización tipo **Line Chart**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     DATE_FORMAT(fecha, 'yyyy-MM') as mes,
# MAGIC     SUM(total) as ingresos_totales,
# MAGIC     COUNT(*) as num_transacciones,
# MAGIC     ROUND(AVG(total), 0) as ticket_promedio
# MAGIC FROM ventas
# MAGIC GROUP BY DATE_FORMAT(fecha, 'yyyy-MM')
# MAGIC ORDER BY mes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏪 Gráfico 2: Comparación de Sucursales
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Gráfico de barras comparando ingresos por sucursal"
# MAGIC
# MAGIC Después de ejecutar, selecciona visualización tipo **Bar Chart**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     s.nombre as sucursal,
# MAGIC     s.ciudad,
# MAGIC     SUM(v.total) as ingresos,
# MAGIC     COUNT(*) as transacciones
# MAGIC FROM ventas v
# MAGIC JOIN sucursales s ON v.sucursal_id = s.sucursal_id
# MAGIC GROUP BY s.nombre, s.ciudad
# MAGIC ORDER BY ingresos DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🍰 Gráfico 3: Distribución por Categoría
# MAGIC
# MAGIC Después de ejecutar, selecciona visualización tipo **Pie Chart**.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     p.categoria,
# MAGIC     SUM(v.total) as ingresos,
# MAGIC     ROUND(SUM(v.total) * 100.0 / (SELECT SUM(total) FROM ventas), 1) as porcentaje
# MAGIC FROM ventas v
# MAGIC JOIN productos p ON v.producto_id = p.producto_id
# MAGIC GROUP BY p.categoria
# MAGIC ORDER BY ingresos DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⏰ Gráfico 4: Mapa de Calor - Ventas por Día y Hora
# MAGIC
# MAGIC 💡 **Pídele al Assistant:**
# MAGIC > "Crea una tabla pivote con los días de la semana como filas y las horas como columnas, mostrando el número de ventas"

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CASE DAYOFWEEK(fecha)
# MAGIC         WHEN 1 THEN '7_Domingo'
# MAGIC         WHEN 2 THEN '1_Lunes'
# MAGIC         WHEN 3 THEN '2_Martes'
# MAGIC         WHEN 4 THEN '3_Miércoles'
# MAGIC         WHEN 5 THEN '4_Jueves'
# MAGIC         WHEN 6 THEN '5_Viernes'
# MAGIC         WHEN 7 THEN '6_Sábado'
# MAGIC     END as dia,
# MAGIC     CAST(SUBSTRING(hora, 1, 2) AS INT) as hora_dia,
# MAGIC     COUNT(*) as ventas
# MAGIC FROM ventas
# MAGIC GROUP BY DAYOFWEEK(fecha), SUBSTRING(hora, 1, 2)
# MAGIC ORDER BY dia, hora_dia

# COMMAND ----------

# MAGIC %md
# MAGIC ## 💰 Gráfico 5: Top 10 Productos Más Vendidos
# MAGIC
# MAGIC Después de ejecutar, selecciona visualización tipo **Bar Chart** horizontal.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     p.nombre as producto,
# MAGIC     p.categoria,
# MAGIC     SUM(v.cantidad) as unidades,
# MAGIC     SUM(v.total) as ingresos
# MAGIC FROM ventas v
# MAGIC JOIN productos p ON v.producto_id = p.producto_id
# MAGIC GROUP BY p.nombre, p.categoria
# MAGIC ORDER BY unidades DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📱 Gráfico 6: Métodos de Pago - ¿El digital supera al efectivo?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     CASE
# MAGIC         WHEN metodo_pago = 'efectivo' THEN 'Efectivo'
# MAGIC         WHEN metodo_pago IN ('nequi', 'daviplata') THEN 'Billetera Digital'
# MAGIC         ELSE 'Tarjeta'
# MAGIC     END as tipo_pago,
# MAGIC     COUNT(*) as transacciones,
# MAGIC     SUM(total) as ingresos
# MAGIC FROM ventas
# MAGIC GROUP BY
# MAGIC     CASE
# MAGIC         WHEN metodo_pago = 'efectivo' THEN 'Efectivo'
# MAGIC         WHEN metodo_pago IN ('nequi', 'daviplata') THEN 'Billetera Digital'
# MAGIC         ELSE 'Tarjeta'
# MAGIC     END
# MAGIC ORDER BY transacciones DESC

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📊 Gráfico 7: Evolución de Sucursales en el Tiempo

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     DATE_FORMAT(v.fecha, 'yyyy-MM') as mes,
# MAGIC     s.nombre as sucursal,
# MAGIC     SUM(v.total) as ingresos
# MAGIC FROM ventas v
# MAGIC JOIN sucursales s ON v.sucursal_id = s.sucursal_id
# MAGIC GROUP BY DATE_FORMAT(v.fecha, 'yyyy-MM'), s.nombre
# MAGIC ORDER BY mes

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🎯 Resumen Ejecutivo - KPIs de Café Origen

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) as total_transacciones,
# MAGIC     SUM(total) as ingresos_totales,
# MAGIC     ROUND(AVG(total), 0) as ticket_promedio,
# MAGIC     COUNT(DISTINCT fecha) as dias_operacion,
# MAGIC     ROUND(SUM(total) / COUNT(DISTINCT fecha), 0) as ingreso_diario_promedio,
# MAGIC     COUNT(DISTINCT sucursal_id) as sucursales_activas
# MAGIC FROM ventas

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ ¡Dashboard completo!
# MAGIC
# MAGIC ### Recomendaciones para Café Origen (basadas en los datos):
# MAGIC 1. **Sucursal estrella** → Identificada con mayor ingreso
# MAGIC 2. **Horas pico** → Optimizar personal en esos horarios
# MAGIC 3. **Productos estrella** → Mantener stock y considerar promociones cruzadas
# MAGIC 4. **Pagos digitales** → Crecimiento de Nequi/Daviplata, considerar incentivos
# MAGIC 5. **Fines de semana** → Ajustar ofertas según el patrón de consumo
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🎓 ¿Qué aprendimos hoy?
# MAGIC - Cómo cargar datos en Databricks
# MAGIC - Exploración de datos con PySpark y SQL
# MAGIC - Transformaciones y análisis de negocio
# MAGIC - Visualizaciones para toma de decisiones
# MAGIC - **¡Todo asistido por IA!** 🤖
