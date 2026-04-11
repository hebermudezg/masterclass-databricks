# Masterclass: Analitica de Datos Asistida por IA

Taller practico con Databricks, Genie y datos reales del ICFES Saber 11.

## La pregunta

> Puede la IA predecir tu puntaje del ICFES solo con saber tu estrato,
> tipo de colegio y si tienes internet en casa?

## Dataset

| Campo | Detalle |
|-------|---------|
| Nombre | Resultados Saber 11 |
| Fuente | [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe) |
| Registros | 27,000+ (periodo 2022) |
| Variables | Estrato, tipo colegio, educacion padres, internet, puntajes |

## Flujo de la masterclass

| Paso | Que hacemos | Herramienta |
|------|-------------|-------------|
| 1 | Cargar datos del ICFES | Notebook 01 (2 lineas) |
| 2 | Guardar como tabla Delta | Notebook 01 |
| 3 | Explorar datos sin codigo | Genie (IA de Databricks) |
| 4 | Entrenar modelo de prediccion | Notebook 02 (Random Forest + MLflow) |
| 5 | Desplegar como API | Notebook 03 (Model Serving) |

## Como usar

1. Crear cuenta en [Databricks Free Edition](https://www.databricks.com/try-databricks)
2. Conectar este repo: pantalla de bienvenida > **Connect to a GitHub repo**
3. Ejecutar notebooks en orden: 01 > 02 > 03

## Estructura

```
dataset/
  icfes_saber11.csv             # Dataset limpio listo para usar
notebooks/
  01_explorar_datos.py          # Carga + Delta + intro a Genie
  02_modelo_prediccion.py       # Feature engineering + ML + MLflow
  03_deploy_produccion.py       # Model Registry + API REST
```

## Links

- Databricks Free: https://www.databricks.com/try-databricks
- Dataset ICFES: https://www.datos.gov.co/d/kgxf-xxbe
- Datos abiertos Colombia: https://www.datos.gov.co
