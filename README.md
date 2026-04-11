# Masterclass: Analitica de Datos Asistida por IA

**Taller practico** | Databricks + ICFES Saber 11 + datos abiertos de Colombia

## La pregunta

> Puede la IA predecir tu puntaje del ICFES solo con saber tu estrato,
> tipo de colegio y si tienes internet en casa?

## Que vamos a construir

Con **7 millones de resultados reales del ICFES Saber 11** (datos.gov.co):

1. **Explorar** patrones de rendimiento academico con visualizaciones y Genie (IA de Databricks)
2. **Entrenar** un modelo de ML que predice el puntaje global
3. **Desplegar** el modelo como API REST en produccion

## Dataset

| Campo | Detalle |
|-------|---------|
| Nombre | Resultados Unicos Saber 11 |
| Fuente | [datos.gov.co](https://www.datos.gov.co/d/kgxf-xxbe) |
| Registros | 7,109,704 (usamos ~50,000 filtrados 2020+) |
| Variables clave | Puntaje global, estrato, educacion padres, tipo colegio, internet, departamento |

## Requisitos

- Cuenta en [Databricks Free Edition](https://www.databricks.com/try-databricks) (gratis, sin tarjeta)
- Para Model Serving (notebook 03): Databricks Pay-As-You-Go

## Estructura

```
notebooks/
  01_explorar_datos.py      # Carga, limpieza, EDA, visualizaciones
  02_modelo_prediccion.py   # Feature engineering + Random Forest + MLflow
  03_deploy_produccion.py   # Model Registry + Serving endpoint + API REST
presentacion/
  guia_paso_a_paso.md       # Guion minuto a minuto para el presentador
scripts/
  descargar_datos.py        # Descarga local del CSV
```

## Como usar

1. Crea cuenta en [Databricks Free Edition](https://www.databricks.com/try-databricks)
2. Importa notebooks: **Workspace > Import > URL de este repo**
3. Ejecuta en orden: 01 -> 02 -> 03

## Links

- Dataset ICFES: https://www.datos.gov.co/d/kgxf-xxbe
- Databricks Free: https://www.databricks.com/try-databricks
- Repo: https://github.com/hebermudezg/masterclass-databricks
