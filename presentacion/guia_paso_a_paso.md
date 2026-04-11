# Guia Paso a Paso - Masterclass: Analitica de Datos con IA

## Narrativa central

> "Hoy vamos a usar 7 millones de resultados REALES del ICFES para responder
> una pregunta incomoda: puede la IA predecir tu puntaje del ICFES solo
> con saber tu estrato, tipo de colegio y si tienes internet en casa?"

---

## Antes de la masterclass (30 min antes)

### Preparar Databricks
1. Entrar a Databricks Free Edition: https://www.databricks.com/try-databricks
2. Conectar el repo de GitHub:
   - En la pantalla de bienvenida, usar **"Connect to a GitHub repo"** (en "Set up your workspace")
   - Pegar la URL: `https://github.com/hebermudezg/masterclass-databricks`
   - Los notebooks aparecen automaticamente en el Workspace
   - **NOTA:** La opcion "Import > URL" NO funciona con github.com en Free Edition.
     Usar siempre "Connect to a GitHub repo" o importar archivos manualmente.
3. Ejecutar Notebook 01 hasta el Paso 3 (guardar tabla Delta) para tener los datos listos
4. Probar que Genie reconoce la tabla `default.icfes_saber11`
5. Ejecutar Notebook 02 completo para verificar que el modelo entrena bien
6. Tomar capturas de pantalla de cada resultado como plan B

### Si vas a hacer deploy (Notebook 03)
- Necesitas Databricks Pay-As-You-Go (no funciona en Free Edition)
- Activa la cuenta paga al menos 1 dia antes
- Costo estimado: ~$2-5 USD por toda la demo

---

## Durante la masterclass (70 minutos)

### Bloque 1: Introduccion (5 min)

**Abrir con la pregunta:**

"Levanten la mano los que presentaron el ICFES. Todos, verdad?
Hoy vamos a hacer algo provocador: tomar miles de resultados reales
del Saber 11 y preguntarle a la IA si puede predecir tu puntaje
ANTES de que presentes el examen. Solo con datos como tu estrato,
tipo de colegio, y si tienes internet."

**Lo que vamos a hacer:**
1. Cargar datos reales y guardarlos en Databricks
2. Explorar con Genie (la IA de Databricks) SIN escribir codigo
3. Crear visualizaciones profesionales con Python
4. Entrenar un modelo de Machine Learning
5. Ponerlo en produccion como API

---

### Bloque 2: Cargar datos + tabla Delta - Notebook 01 (5 min)

**Celda: Cargar datos (1 min)**
- Ejecutar. "Son datos reales del ICFES, 27,000 estudiantes"

**Celda: Ver los datos (1 min)**
- "Miren las columnas: estrato, tipo de colegio, educacion de los padres, internet, puntajes"

**Celda: Guardar como tabla Delta (2 min)**
- Explicar brevemente que es Delta Lake: formato nativo de Databricks, permite que Genie y SQL accedan a los datos
- Ejecutar

**Celda SQL: Verificar (1 min)**
- "Listo, la tabla esta creada. Ahora viene lo bueno."

---

### Bloque 3: GENIE - Explorar SIN codigo (20 min) - PROTAGONISTA

**Transicion:**
"Ahora voy a cerrar el notebook por un momento y vamos a abrir Genie.
Genie es el asistente de IA de Databricks. Le voy a hacer preguntas
sobre nuestros datos en espanol, en lenguaje natural, y el va a generar
el SQL y las graficas por nosotros."

**Como abrir Genie:**
- Menu lateral izquierdo > **Genie** (bajo la seccion SQL)
- Seleccionar la tabla `default.icfes_saber11`

**Secuencia de preguntas (seguir este orden, construye una narrativa):**

**Calentamiento (3 min):**
1. "Cuantos estudiantes hay en total?"
   - Genie responde con SQL: `SELECT COUNT(*) FROM ...`
   - "Miren: genero el SQL solito"

2. "Cual es el puntaje promedio?"
   - Comentar el resultado

3. "Cuantos estudiantes hay por estrato?"
   - "Vean la distribucion: la mayoria esta en estrato 1 y 2"

**El descubrimiento - momento clave (7 min):**

4. **"Cual es el puntaje promedio por estrato socioeconomico?"**
   - ANTES de ejecutar: "Ustedes que creen? Cuanta diferencia habra?"
   - Ejecutar y PAUSAR. Dejar que la grafica hable.
   - "De estrato 1 a estrato 6 hay X puntos de diferencia"
   - "Eso no es opinion, son datos"

5. "Hay diferencia entre colegios OFICIAL y NO OFICIAL?"
   - Dejar reaccionar

6. "Los estudiantes con internet en casa tienen mejor puntaje?"
   - "Internet cambia X puntos en promedio"

7. "Como afecta la educacion de la madre al puntaje?"
   - "Miren como sube el puntaje con cada nivel educativo de la mama"

**Profundizando (5 min):**

8. "Que porcentaje de estudiantes de Estrato 1 supera los 300 puntos?"
   - Dato fuerte para la reflexion

9. "Cuales son los 10 departamentos con mejor puntaje promedio?"
   - "Busquen el suyo"

10. "Cual es el puntaje promedio de ingles por estrato?"
    - Otra dimension interesante

**Momento audiencia (5 min):**

11. Preguntar al publico: **"Que quieren saber de los datos?"**
    - Escribir en Genie lo que digan
    - Este es el momento mas interactivo y memorable
    - Si nadie dice nada: "Que tal si miramos la diferencia entre jornada manana y noche?"

**Reflexion:**
"Acabamos de analizar miles de resultados del ICFES sin escribir
UNA sola linea de codigo. Genie genero todo el SQL. Eso es
analitica de datos asistida por IA."

---

### Bloque 4: Modelo de ML - Notebook 02 (25 min)

**Transicion (2 min):**
"Ahora la pregunta real: puede un modelo PREDECIR el puntaje?
Le vamos a dar SOLO variables socioeconomicas. Nada de puntajes por materia.
Estrato, educacion de los padres, tipo de colegio, internet...
Si el modelo puede predecir con eso, que nos dice del sistema educativo?"

**Celda: Feature engineering (3 min)**
- "Convertimos texto a numeros: Estrato 1 = 1, Postgrado = 9"
- "12 variables. Ninguna es academica. Solo contexto socioeconomico."

**Celda: Train/test split (1 min)**
- "80% para que aprenda, 20% para evaluarlo"

**Celda: Entrenar con MLflow (5 min)**
- Ejecutar y esperar
- Interpretar:
  - "MAE de X: se equivoca en promedio por X puntos"
  - "R2: explica el X% de la variacion en tu puntaje"
  - "Piensen: SIN saber nada de tu capacidad, solo con datos socioeconomicos..."

**Celda: Feature importance (4 min) - SEGUNDO MOMENTO CLAVE**
- "Que es lo que MAS importa segun el modelo?"
- Generar debate

**Celda: Prediccion en vivo (5 min) - MOMENTO INTERACTIVO**
- Perfil A vs Perfil B: mostrar el contraste
- "Alguien quiere probar con su propio perfil?"
- Modificar valores en vivo

---

### Bloque 6: Deploy a produccion - Notebook 03 (5 min)

*Si tienes cuenta paga, mostrar en vivo. Si no, mostrar capturas.*

- "El modelo es ahora una API que cualquier app puede consultar"
- "Una secretaria de educacion podria usar esto para identificar estudiantes en riesgo"
- Mostrar el curl de ejemplo

---

### Bloque 7: Cierre (5 min)

**Recapitular:**
"En 1 hora hicimos todo el ciclo:
1. Cargamos datos reales del ICFES
2. Exploramos con Genie SIN codigo
3. Creamos graficas profesionales con Python
4. Entrenamos un modelo de IA
5. Lo pusimos en produccion

Y descubrimos que las condiciones socioeconomicas predicen una
parte significativa del puntaje academico."

**Reflexion:**
"Los datos no tienen opinion politica. Pero los patrones que revelan
deberian informar politicas publicas. La IA no reemplaza al analista: lo potencia."

**Compartir:**
- Databricks Free: https://www.databricks.com/try-databricks
- Datos abiertos: https://www.datos.gov.co
- Dataset ICFES: https://www.datos.gov.co/d/kgxf-xxbe
- Este repo: https://github.com/hebermudezg/masterclass-databricks

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| Descarga lenta de CSV | Reducir $limit a 20000 o usar Volume pre-cargado |
| Genie no encuentra la tabla | Verificar que se ejecuto el Paso 3 (saveAsTable) |
| Genie responde en ingles | Escribir las preguntas en espanol, suele responder en el mismo idioma |
| Error MLflow | Verificar que tiene `mlflow.set_registry_uri("databricks-uc")` |
| Model Serving falla | Solo funciona en tier pago, mostrar capturas |
| Notebook lento | Reducir datos: cambiar $limit a 10000 |

## Codigos rapidos de referencia

**Estrato:** 1-6 (Sin Estrato = 0)
**Educacion padres:** Ninguno=0, Primaria inc.=1, Primaria comp.=2, Bach. inc.=3, Bach. comp.=4, Tecnica inc.=5, Tecnica comp.=6, Profesional inc.=7, Profesional comp.=8, Postgrado=9
**Colegio:** Oficial=1, Privado=0 | Rural=1, Urbano=0 | Bilingue=1, No=0
**Personas hogar:** 1a2=1, 3a4=2, 5a6=3, 7a8=4, 9+=5
