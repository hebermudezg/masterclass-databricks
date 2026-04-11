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
3. Ejecutar Notebook 01 completo (la descarga de datos toma ~1 minuto)
4. Ejecutar Notebook 02 completo (el modelo entrena en ~30 segundos)
5. Verificar que las graficas se generen correctamente
6. Tomar capturas de pantalla de cada resultado como plan B

### Si vas a hacer deploy (Notebook 03)
- Necesitas Databricks Pay-As-You-Go
- Activar cuenta paga al menos 1 dia antes
- Ejecutar Notebook 03 para verificar que Model Serving funcione
- El endpoint tarda ~5 minutos en estar listo

---

## Durante la masterclass (70 minutos)

### Bloque 1: Introduccion (5 min)

**Abrir con la pregunta:**
"Levanten la mano los que presentaron el ICFES. Todos, verdad?
Hoy vamos a hacer algo interesante: tomar 7 millones de resultados
reales del Saber 11 y preguntarle a un modelo de IA si puede predecir
tu puntaje ANTES de que presentes el examen. Solo con datos como tu
estrato, si tu colegio es oficial o privado, y si tienes internet en casa."

**Que vamos a hacer:**
1. Explorar los datos con visualizaciones y con Genie (la IA de Databricks)
2. Entrenar un modelo de Machine Learning
3. Ponerlo en produccion como una API

"Todo esto en 1 hora, con datos reales, en una plataforma gratuita."

---

### Bloque 2: Exploracion de datos - Notebook 01 (25 min)

**Celda: Cargar datos (2 min)**
- "Estamos descargando 50,000 resultados recientes directamente de datos.gov.co"
- "El dataset completo tiene 7 millones, pero para la demo usamos una muestra"
- Mostrar el resultado: filas x columnas

**Celda: Grupos de columnas (2 min)**
- "Miren como se organizan: datos del colegio, del estudiante, de la familia, y los puntajes"
- "Lo interesante son las variables de la familia: estrato, educacion de los padres, internet..."

**Celda: Limpieza (2 min)**
- "Eliminamos duplicados y convertimos puntajes a numeros"
- Comentar las estadisticas basicas

**Celda: Distribucion del puntaje (2 min)**
- "Asi se distribuyen los puntajes. El promedio es de ~XXX puntos"
- "Miren que es una campana bastante normal"

**Celda: Puntaje por estrato - EL MOMENTO CLAVE (5 min)**
- PAUSAR antes de ejecutar: "Antes de ver el resultado, ustedes que creen?
  Cuanta diferencia habra entre estrato 1 y estrato 6?"
- Ejecutar y dejar que la grafica hable
- "Miren esos numeros. De estrato 1 a estrato 6 hay X puntos de diferencia"
- "Eso es un dato, no una opinion"

**Celda: 4 comparaciones (5 min)**
- Ir grafica por grafica:
- "Oficial vs privado: hay diferencia? Cuanta?"
- "Urbano vs rural: ahi esta"
- "Internet en casa: miren lo que cambia"
- "Por genero: hay diferencia pero es menor que el estrato"

**Celda: Educacion de la madre (3 min)**
- "Este es poderoso: la educacion de la mama impacta directamente"
- "De 'Ninguno' a 'Postgrado' hay X puntos de diferencia"
- "Esto no es solo un dato, es un argumento para politica publica"

**Celda: Departamentos (2 min)**
- "Busquen su departamento. Los rojos son los 5 mas bajos, los verdes los 5 mas altos"

**Demo Genie (3-5 min)**
- Abrir Genie en el panel lateral
- "Ahora voy a preguntarle a la IA directamente"
- Escribir: "Cual es el puntaje promedio por estrato y tipo de colegio?"
- Mostrar como genera SQL y grafica automaticamente
- PREGUNTAR A LA AUDIENCIA: "Que quieren preguntarle?" -> escribir lo que digan
- Enfatizar: "Genie CONOCE tu tabla. Sabe que columnas tienes, los valores posibles..."

---

### Bloque 3: Modelo de ML - Notebook 02 (25 min)

**Intro (2 min)**
- "Ahora la pregunta real: puede un modelo PREDECIR el puntaje?"
- "Le vamos a dar SOLO variables socioeconomicas. Nada de puntajes por materia."
- "Estrato, educacion de los padres, tipo de colegio, internet, computador..."
- "Si el modelo puede predecir con eso, que nos dice del sistema educativo?"

**Celda: Feature engineering (3 min)**
- "Convertimos texto a numeros: Estrato 1 = 1, Postgrado = 9, Si = 1, No = 0"
- Mostrar la lista de 12 features
- "12 variables. Ninguna es el puntaje de una materia. Solo contexto socioeconomico"

**Celda: Train/test split (1 min)**
- "80% para que el modelo aprenda, 20% para evaluarlo con datos que nunca vio"

**Celda: Entrenar con MLflow (5 min)**
- "Random Forest: le preguntamos a 200 arboles de decision"
- "MLflow registra TODO automaticamente"
- Ejecutar y esperar resultado
- INTERPRETAR las metricas en terminos simples:
  - "MAE de X: el modelo se equivoca en promedio por X puntos"
  - "R2 de 0.XX: solo con saber tu estrato y si tienes internet,
     el modelo explica el XX% de la variacion en tu puntaje"
- REFLEXION: "Piensen en eso. Sin saber NADA de tu capacidad academica,
  solo con datos socioeconomicos, ya predice una parte significativa"

**Celda: Feature importance (5 min) - SEGUNDO MOMENTO CLAVE**
- "Que es lo que MAS importa segun el modelo?"
- Ejecutar y analizar
- "Miren: [variable X] es la mas importante"
- Generar debate: "Esto les sorprende? Que les dice del sistema?"

**Celda: Prediccion vs Realidad (2 min)**
- "Puntos cerca de la linea roja = buenas predicciones"
- "No es perfecto, y eso es bueno: significa que HAY espacio para que
   un estudiante supere su contexto socioeconomico"

**Celda: Registrar modelo (1 min)**
- "Guardamos el modelo en MLflow para produccion"

**Celda: Prediccion en vivo (5 min) - MOMENTO INTERACTIVO**
- Mostrar los dos perfiles contrastantes
- "Perfil A: estrato 1, colegio rural, sin internet..."
- "Perfil B: estrato 5, privado bilingue, con internet..."
- Ejecutar y mostrar la diferencia
- PREGUNTAR: "Alguien quiere probar con su propio perfil?"
- Modificar valores en vivo segun lo que diga la audiencia

---

### Bloque 4: Deploy a produccion - Notebook 03 (10 min)

**Intro (2 min)**
- "Ahora el paso final: convertir este modelo en una API"
- "Imaginense que la Secretaria de Educacion quiere identificar
   estudiantes en riesgo ANTES del examen para enviar tutores"
- "Este modelo podria ser la base de esa herramienta"

**Celda: Crear endpoint (3 min)**
- Ejecutar (o mostrar pre-ejecutado)
- "Databricks crea un servidor automaticamente"
- "Scale-to-zero: si nadie lo usa, no pagas"

**Celda: Probar endpoint (3 min)**
- Ejecutar prediccion en vivo
- "El modelo esta respondiendo como servicio web"
- Mostrar el curl de ejemplo

**Celda: Caso de uso (2 min)**
- "Cualquier aplicacion puede llamar esta API"
- "Una plataforma web, una app movil, un dashboard de Power BI"

---

### Bloque 5: Cierre (5 min)

**Recapitular:**
- "En 1 hora: datos abiertos del ICFES -> analisis -> modelo de IA -> API en produccion"
- "Descubrimos patrones reales de desigualdad educativa"
- "Y construimos una herramienta que podria ayudar a combatirla"

**Reflexion:**
- "Los datos no tienen opinion politica. Pero los patrones que revelan
   deberian informar politicas publicas"
- "La IA no reemplaza al analista: lo potencia"

**Recursos:**
- Databricks Free: https://www.databricks.com/try-databricks
- Datos abiertos: https://www.datos.gov.co
- Dataset ICFES: https://www.datos.gov.co/d/kgxf-xxbe
- Este repo: https://github.com/hebermudezg/masterclass-databricks

**Cerrar con preguntas**

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| Descarga lenta de CSV | Reducir $limit a 20000 o usar Volume pre-cargado |
| Duplicados en datos | drop_duplicates ya esta en el codigo |
| Genie no responde | Recargar pagina, verificar que la tabla Delta existe |
| Model Serving no disponible | Solo funciona en tier pago, mostrar capturas |
| Notebook lento | Reducir datos: cambiar $limit a 10000 |
| Error de memoria | Reiniciar cluster o reducir datos |

## Codigos rapidos de referencia

**Estrato:** 1-6 (Sin Estrato = 0)
**Educacion padres:** Ninguno=0, Primaria inc.=1, Primaria comp.=2, Bachillerato inc.=3, Bachillerato comp.=4, Tecnica inc.=5, Tecnica comp.=6, Profesional inc.=7, Profesional comp.=8, Postgrado=9
**Colegio:** Oficial=1, Privado=0 | Rural=1, Urbano=0 | Bilingue=1, No=0
**Personas hogar:** 1a2=1, 3a4=2, 5a6=3, 7a8=4, 9+=5
