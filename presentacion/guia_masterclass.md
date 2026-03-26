# Guia del Presentador - Master Class Cafe Origen

## Formato: Demo en vivo (tu presentas, ellos observan)

La audiencia NO necesita cuenta ni seguir en su computador.
Tu haces todo en pantalla compartida. Ellos aprenden observando.
Al final les compartes los archivos para que repliquen en su tiempo.

---

## Antes de la sesion (preparacion)

### Tu setup (hacer antes del 16 de abril):
1. **Databricks:** Crear cuenta Community Edition, cluster listo, CSVs subidos, notebooks importados
2. **Streamlit:** Dashboard desplegado en Streamlit Cloud con URL publica
3. **Backup:** Screenshots de cada resultado por si el cluster falla
4. **Probar:** Ejecutar los 4 notebooks completos al menos una vez antes

### Lo que compartes DESPUES de la sesion:
- Link al repo de GitHub (con notebooks + CSV + Streamlit app)
- Link al dashboard desplegado
- Esta guia si quieren

---

## LA HISTORIA

El hilo narrativo de toda la sesion es este:

> **Tu eres el nuevo analista de datos de "Cafe Origen"**, una cadena de cafeterias colombiana
> con 5 sucursales. La gerente general, Dona Marta, te contrato porque las ventas han estado
> raras y necesita respuestas ANTES de decidir si abre una 6ta sucursal.
>
> Tu mision: en 2 horas, darle a Dona Marta un reporte con datos que la ayude a decidir.
> Tu arma secreta: Databricks + Inteligencia Artificial.

Cada bloque responde una pregunta de "Dona Marta". Esto le da ritmo y proposito a todo.

---

## BLOQUE 1: Intro - "Dona Marta nos contrato" (10 min)

### Que decir:

> "Buenas noches a todos. Imaginen esto: los acaban de contratar como analistas de datos
> en Cafe Origen, una cadena de cafeterias colombiana. La gerente, Dona Marta, les dice:
> 'Necesito saber como van mis ventas, que producto me da mas plata, y si deberia abrir
> otra sucursal. Tienen hasta manana.'
>
> Hoy vamos a resolver eso EN VIVO. Vamos a usar Databricks, que es una plataforma
> profesional de analisis de datos en la nube, y vamos a dejar que la IA nos escriba
> el codigo. Lo unico que necesitamos es hacer las preguntas correctas."

### Puntos rapidos:
- **Databricks** = notebook en la nube con superpoderes (Apache Spark)
- **Databricks Assistant** = IA que genera codigo PySpark/SQL a partir de texto
- **Community Edition** = gratis, sin tarjeta de credito
- Hoy NO van a necesitar abrir nada. Solo observen. Les comparto todo despues.

---

## BLOQUE 2: "Primero, veamos que datos tenemos" (15 min)

### Dona Marta dice:
> "Aqui tienen los datos de ventas de los ultimos 9 meses. Haganle."

### Ejecutar notebook 00_setup:
1. Mostrar rapidamente los 3 archivos CSV en pantalla
2. Ejecutar la carga - comentar cada paso
3. Mostrar las 3 tablas: ventas (4,700 registros), productos (20), sucursales (5)

### Narrar:
> "Fijense: 3 lineas de codigo y ya tenemos casi 5,000 registros listos.
> En Excel esto seria facil, pero imaginen con 50 millones de registros.
> Ahi es donde Databricks brilla."

### Mostrar las vistas temporales SQL:
> "Ahora podemos hablarle a estos datos en SQL, que es como el idioma universal de los datos."

---

## BLOQUE 3: "Dona Marta quiere el panorama general" (25 min)

### Dona Marta dice:
> "Dame el panorama. Cuantas ventas tenemos? Cuando vendemos mas? Que se vende mas?"

### Ejecutar notebook 01_exploracion:

**Para cada analisis, seguir este patron:**
1. Plantear la pregunta de Dona Marta
2. Abrir el Databricks Assistant
3. Escribir el prompt EN ESPANOL (que la audiencia lo vea)
4. El Assistant genera el codigo
5. Ejecutar y mostrar resultado
6. Interpretar: "Esto le dice a Dona Marta que..."

### Los prompts en vivo al Assistant:

**Prompt 1:** "Muestrame las estadisticas descriptivas de las ventas"
> Interpretar: "El ticket promedio es de $X, pero hay ventas desde $Y hasta $Z. Hay variabilidad."

**Prompt 2:** "Cuantas ventas hay por mes? Ordena cronologicamente"
> Interpretar: "Miren, en diciembre subio / en enero bajo. Tiene sentido por la temporada."

**Prompt 3:** "Cual es el metodo de pago mas usado?"
> Interpretar: "Nequi ya esta compitiendo con efectivo. Dona Marta deberia incentivar digital."

**Prompt 4:** "A que hora del dia se vende mas?"
> Interpretar: "Hay un pico a las X. Dona Marta deberia tener mas personal a esa hora."

**Prompt 5:** "Top 5 productos mas vendidos haciendo join con la tabla de productos"
> Interpretar: "El Espresso es rey. Pero vendemos mucho Croissant tambien. Combo perfecto."

### Frase clave:
> "Fijense que NO memorice la sintaxis de PySpark. Le pedi a la IA en espanol
> y ella genero el codigo. Mi trabajo como analista es hacer las PREGUNTAS CORRECTAS
> e INTERPRETAR los resultados. Eso no lo hace la IA por mi."

---

## BLOQUE 4: "Dona Marta quiere respuestas de negocio" (25 min)

### Dona Marta dice:
> "Ok, ya vi los numeros generales. Ahora dime: cual sucursal me da mas plata?
> Que producto es el mas rentable? Y el fin de semana vendemos mas o menos?"

### Ejecutar notebook 02_transformaciones:

**Analisis 1: Sucursal mas rentable**
- Ejecutar la consulta
- Hacer notar: "La que mas vende NO siempre es la mas rentable. Miren el ticket promedio."
- Comparar premium vs estandar
> "Dona Marta, la sucursal del Centro vende mas, pero Poblado tiene mejor ticket promedio. Si quiere abrir otra, deberia ser formato premium."

**Analisis 2: Categorias por margen**
- Ejecutar el analisis
- Hacer notar el margen de cada categoria
> "Las bebidas calientes tienen 70% de margen. La comida tiene 60%. Dona Marta, su negocio es el CAFE, no la comida."

**Analisis 3: Semana vs fin de semana**
- Ejecutar la comparacion
> "Entre semana se vende mas volumen. Pero el fin de semana el ticket es mas alto. La gente se consiente mas el sabado."

**Analisis 4: Top productos por ganancia**
- Ejecutar el ranking
> "Ojo: el Cappuccino no es el mas vendido, pero es el que mas ganancia genera por unidad. Dona Marta deberia promocionarlo mas."

### Momento IA impro:
Abrir una celda nueva y preguntarle al Assistant algo no planeado:
> "Cual sucursal tiene la mayor caida de ventas en los ultimos 3 meses?"

Mostrar que la IA resuelve preguntas al vuelo.

---

## BLOQUE 5: "El reporte para Dona Marta" (20 min)

### Dona Marta dice:
> "Todo eso esta muy lindo en codigo, pero yo necesito GRAFICOS. Algo que pueda
> mostrarle a los inversionistas."

### Ejecutar notebook 03_visualizacion:

Ir ejecutando los graficos uno a uno. Para cada uno:
1. Ejecutar la celda SQL
2. Click en el icono de grafico
3. Seleccionar el tipo de visualizacion
4. Narrar lo que el grafico revela

**Graficos clave y que decir:**

1. **Tendencia mensual (lineas):** "Estamos creciendo? Miren la tendencia..."
2. **Ranking sucursales (barras):** "Quien va ganando la carrera?"
3. **Categorias (pastel/dona):** "De donde viene el dinero de Cafe Origen?"
4. **Mapa de calor (heatmap):** "ESTE es mi favorito. Muestra exactamente CUANDO vender. Miren el lunes a las 11am vs el sabado a las 3pm."
5. **Top productos (barras):** "Estos son los jugadores estrella."
6. **Metodos de pago:** "El efectivo esta muriendo? Los datos dicen que..."
7. **KPIs finales:** "Si Dona Marta tiene 30 segundos, esto es lo que ve."

### Frase de transicion:
> "Muy bien, ya tenemos todo el analisis en Databricks. Pero Dona Marta no va a abrir
> Databricks. Ella quiere un LINK. Algo bonito que pueda abrir en su celular.
> Y aqui viene la cereza del pastel..."

---

## BLOQUE 6: "El dashboard desplegado" - CIERRE WOW (15 min)

### Que decir:
> "Les presento el dashboard de Cafe Origen. Esto esta DESPLEGADO en internet.
> Cualquiera con el link puede verlo. No necesita cuenta, no necesita instalar nada."

### Abrir el dashboard de Streamlit en el navegador:
- Mostrar la URL publica
- Recorrer cada seccion del dashboard
- Jugar con los filtros (cambiar sucursal, categoria, fechas)
- Mostrar como los KPIs se actualizan en tiempo real

### Explicar (rapido, sin entrar en detalle de codigo):
> "Esto lo hice con Streamlit, que es una herramienta de Python para crear dashboards.
> Se despliega gratis en Streamlit Cloud. El codigo tiene menos de 300 lineas.
> Y los datos son los MISMOS que analizamos en Databricks."

### Mostrar el flujo completo:
> "Entonces el proceso profesional real es:
> 1. Los datos llegan (CSVs, bases de datos, APIs)
> 2. Los analizas en Databricks con ayuda de IA
> 3. Construyes un dashboard para que el negocio lo vea
> 4. Lo despliegas para que cualquiera acceda con un link
>
> Y eso es EXACTAMENTE lo que hicimos hoy en menos de 2 horas."

---

## BLOQUE 7: Conclusiones (10 min)

### Resumen:
> "Hoy aprendimos 4 cosas:"
1. **Databricks** para analizar datos a escala, gratis
2. **IA (Assistant)** para generar codigo sin memorizarse nada
3. **Hacer las preguntas correctas** es mas importante que saber la sintaxis
4. **Desplegar resultados** para que el negocio los use

### Mensaje final:
> "La IA no reemplaza al analista de datos. La IA genera el codigo, pero USTEDES
> son los que hacen las preguntas correctas, interpretan los resultados y toman
> las decisiones. Dona Marta no necesita alguien que sepa PySpark de memoria.
> Necesita alguien que entienda su negocio y sepa que preguntar.
> Esa persona pueden ser ustedes."

### Compartir:
- Link al repo de GitHub con todo el material
- Link al dashboard de Streamlit
- "Todo esto es gratis. Pueden replicarlo esta misma noche."

---

## Tips de presentacion

- **NO correr.** Es mejor cubrir menos y que entiendan bien
- **Narrar todo.** No ejecutar codigo en silencio. Siempre explicar que hace y por que
- **Errores son normales.** Si algo falla, mostrar como el Assistant ayuda a debuggear
- **Backup:** Tener screenshots de cada resultado por si el cluster se cae
- **Internet:** Verificar conexion estable. Todo es cloud
- **Agua.** Son 2 horas hablando. Llevar agua
