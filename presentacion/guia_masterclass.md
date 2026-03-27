# Guia del Presentador - Master Class Cafe Origen

## Formato: Demo en vivo (tu presentas, ellos observan)
## Plataforma: Databricks Trial (Premium) - TODO dentro de Databricks

---

## Antes de la sesion

### Timeline:
- **14 abril:** Activar trial de Databricks (ver `guia_trial_databricks.md`)
- **14-15 abril:** Subir datos, ejecutar notebooks, crear dashboard y Genie
- **16 abril 7PM:** Master class

### Tu setup:
1. Trial activado, workspace funcionando
2. SQL Warehouse encendido
3. CSVs subidos, notebooks importados
4. Notebook 04_sql_dashboard ejecutado (tablas creadas)
5. SQL Dashboard creado y con graficos
6. Genie Space configurado con la tabla `cafe_origen.ventas_completas`
7. Todo probado al menos una vez

### Tener abiertos:
- Tab 1: Notebook 00_setup
- Tab 2: Notebook 01_exploracion
- Tab 3: Notebook 02_transformaciones
- Tab 4: SQL Dashboard
- Tab 5: Genie

---

## LA HISTORIA

> **Tu eres el nuevo analista de datos de "Cafe Origen"**, una cadena de cafeterias colombiana
> con 5 sucursales. La gerente general, Dona Marta, te contrato porque las ventas han estado
> raras y necesita respuestas ANTES de decidir si abre una 6ta sucursal.
>
> Tu mision: darle a Dona Marta un reporte con datos.
> Tu arma secreta: Databricks + Inteligencia Artificial.

---

## BLOQUE 1: "Dona Marta nos contrato" (10 min)

### Que decir:

> "Buenas noches. Imaginen esto: los acaban de contratar como analistas de datos
> en Cafe Origen, una cadena de cafeterias colombiana. La gerente, Dona Marta, les dice:
> 'Necesito saber como van mis ventas, que producto me da mas plata, y si deberia abrir
> otra sucursal.'
>
> Hoy vamos a resolver eso EN VIVO usando Databricks, que es una plataforma profesional
> de datos, y vamos a dejar que la Inteligencia Artificial nos escriba el codigo."

### Puntos clave:
- **Databricks** = plataforma unificada de datos. Netflix, Shell, T-Mobile la usan.
- **Databricks Assistant** = IA integrada que genera codigo a partir de texto
- **Genie** = IA que responde preguntas de negocio sin codigo (el wow del final)
- Hoy NO necesitan abrir nada. Solo observen.

---

## BLOQUE 2: "Veamos que datos tenemos" (15 min)

### Dona Marta dice:
> "Aqui tienen los datos de ventas de los ultimos 9 meses."

### Ejecutar notebook 00_setup:
- Mostrar los 3 CSVs rapidamente
- Ejecutar la carga
- Mostrar las tablas: ventas (4,700), productos (20), sucursales (5)

### Narrar:
> "3 lineas de codigo y ya tenemos casi 5,000 registros listos para analizar.
> En Excel esto seria facil, pero imaginen con 50 millones de registros...
> Ahi es donde Databricks brilla."

---

## BLOQUE 3: "El panorama general" (25 min)

### Dona Marta dice:
> "Dame el panorama. Cuantas ventas? Cuando vendemos mas? Que se vende mas?"

### Ejecutar notebook 01_exploracion

**Patron para cada analisis:**
1. Plantear la pregunta de Dona Marta
2. Abrir el Databricks Assistant
3. Escribir el prompt en espanol (que la audiencia lo vea)
4. El Assistant genera el codigo
5. Ejecutar y mostrar resultado
6. Interpretar: "Esto le dice a Dona Marta que..."

### Prompts al Assistant:
- "Muestrame las estadisticas descriptivas de las ventas"
- "Cuantas ventas hay por mes? Ordena cronologicamente"
- "Cual es el metodo de pago mas usado?"
- "A que hora del dia se vende mas?"
- "Top 5 productos mas vendidos con join a la tabla de productos"

### Frase clave:
> "No memorice la sintaxis de PySpark. Le pedi a la IA en espanol y ella
> genero el codigo. Mi trabajo es hacer las PREGUNTAS CORRECTAS e
> INTERPRETAR los resultados."

---

## BLOQUE 4: "Respuestas para Dona Marta" (25 min)

### Dona Marta dice:
> "Cual sucursal me da mas plata? Que producto es el mas rentable?
> El fin de semana vendemos mas o menos?"

### Ejecutar notebook 02_transformaciones:

**Analisis 1: Sucursal mas rentable**
> "La que mas vende NO siempre es la mas rentable. Miren el ticket promedio.
> Dona Marta, si quiere abrir otra sucursal, deberia ser formato premium."

**Analisis 2: Categorias por margen**
> "Las bebidas calientes tienen 70% de margen. La comida tiene 60%.
> Dona Marta, su negocio es el CAFE, no la comida."

**Analisis 3: Semana vs fin de semana**
> "Entre semana se vende mas volumen. Fin de semana, el ticket es mas alto."

**Analisis 4: Top productos por ganancia**
> "El Cappuccino no es el mas vendido, pero genera mas ganancia por unidad."

### Momento impro con el Assistant:
Abrir celda nueva, preguntar algo no planeado:
> "Cual sucursal tiene la mayor caida de ventas en los ultimos 3 meses?"

---

## BLOQUE 5: "El dashboard para Dona Marta" - PRIMER WOW (20 min)

### Dona Marta dice:
> "Todo eso esta muy lindo en codigo, pero yo necesito GRAFICOS.
> Algo que pueda mostrarle a los inversionistas."

### Cambiar a la tab del SQL Dashboard:
- Mostrar el dashboard ya construido (lo preparaste antes)
- Recorrer cada grafico explicando que muestra
- Mostrar los filtros interactivos

### Narrar:
> "Esto es un SQL Dashboard de Databricks. Tiene su propia URL.
> Dona Marta puede abrirlo desde su celular, sin instalar nada, sin correr codigo.
> Se actualiza automaticamente cuando llegan datos nuevos."

### Mostrar la URL compartible:
- Click en Share
- Mostrar que genera un link
> "Esto es lo que Dona Marta recibe: un link. Asi de simple."

### Mostrar como se crea (rapido):
- Abrir un widget
- Mostrar la consulta SQL detras
- Mostrar como se cambia el tipo de grafico
> "Cada grafico es una consulta SQL. Las mismas que escribimos antes."

---

## BLOQUE 6: "Genie: la IA responde" - CIERRE WOW (15 min)

### Que decir:
> "Pero que tal si Dona Marta no quiere un dashboard fijo?
> Que tal si ella quiere PREGUNTAR lo que se le ocurra?
> Para eso existe Genie."

### Cambiar a la tab de Genie:

### Preguntas en vivo (escribirlas una a una):
1. "Cual es la sucursal con mas ventas?"
2. "Que producto tiene el mejor margen de ganancia?"
3. "Como se comparan las ventas de diciembre vs enero?"
4. "A que hora se vende mas cafe?"
5. "Muéstrame las ventas del ultimo mes por sucursal"

### Para cada pregunta:
- Escribir en lenguaje natural
- Genie genera la consulta SQL y el resultado
- Mostrar que genera graficos automaticamente
- Interpretar el resultado

### Momento interactivo (UNICO momento de participacion):
> "Alguien quiere hacerle una pregunta a Genie sobre Cafe Origen?"

Tomar 2-3 preguntas del publico y escribirlas en Genie en vivo.

### Frase de cierre de Genie:
> "Fijense lo que acaba de pasar: una persona SIN conocimiento tecnico
> le hizo una pregunta en espanol a una IA, y la IA fue a la base de datos,
> genero la consulta, ejecuto el analisis y devolvio la respuesta.
> ESTO es el futuro del analisis de datos."

---

## BLOQUE 7: Conclusiones (10 min)

### Resumen:
> "Hoy Dona Marta recibio:"
1. **Exploracion de datos** con Databricks Assistant (la IA escribe el codigo)
2. **Analisis de negocio** que responde preguntas reales
3. **Un dashboard profesional** con URL compartible
4. **Genie** para hacer preguntas sin codigo

### Mensaje final:
> "La IA no reemplaza al analista de datos. La IA genera el codigo, pero USTEDES
> son los que hacen las preguntas correctas, interpretan los resultados y toman
> las decisiones. Dona Marta no necesita alguien que sepa PySpark de memoria.
> Necesita alguien que entienda su negocio y sepa que preguntar.
> Esa persona pueden ser ustedes."

### Compartir:
- Link al repositorio de GitHub con todo el material
- Link al dashboard (si aun esta activo)
- "Todo el codigo esta en GitHub. Pueden replicarlo."

---

## Plan B: Si algo falla

| Problema | Solucion |
|----------|---------|
| Cluster no enciende | Tener screenshots de cada resultado |
| SQL Warehouse lento | Ya tener el dashboard cargado, no hacer refresh |
| Genie no responde bien | Tener preguntas pre-probadas que sabes que funcionan |
| Internet se cae | Tener los notebooks exportados como HTML en local |
| Trial expiro | Volver a Community Edition + Streamlit (carpeta streamlit-app) |

---

## Tips
- **NO correr.** Mejor cubrir menos y que entiendan
- **Narrar todo.** No ejecutar codigo en silencio
- **Errores son normales.** Mostrar como el Assistant ayuda a debuggear
- **Agua.** Son 2 horas hablando
- **Apagar recursos al terminar.** SQL Warehouse + cluster = consume creditos
