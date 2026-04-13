# Masterclass: Analitica de Datos Asistida por IA

## Proyecto
Masterclass para UNAC (Corporacion Universitaria Adventista de Colombia).
Fecha: 16 abril 2026, 7:00 PM. Duracion: 1h 10min. Virtual.

## Dataset
ICFES Saber 11 (datos.gov.co, ID: kgxf-xxbe). 19,834 estudiantes, 22 columnas, 0 NaN.
CSV limpio en `dataset/icfes_saber11.csv`.

## Notebooks (Databricks Free Edition)
- `01_explorar_datos.py` - Carga CSV de GitHub, guarda como tabla Delta, intro a Genie
- `02_modelo_prediccion.py` - 4 prompts para el Databricks Assistant (Regresion Lineal, Gradient Boosting, comparacion + importancia + prediccion, guardar en MLflow)
- `03_deploy_produccion.py` - 2 prompts para cargar modelo de MLflow y predecir 3 perfiles

## Archivos locales (no en repo)
- `presentacion/script_presentador.md` - Guion minuto a minuto + conceptos clave + preguntas frecuentes + troubleshooting
- `presentacion/backup_notebook_02.py` - Backup con codigo pre-escrito
- `huggingface-app/` - App Gradio desplegada en huggingface.co/spaces/hebermudezg/unac

## Flujo de la charla
1. Intro: colaboracion humano-maquina, que es Databricks (min 0-10)
2. NB01: cargar datos + Delta + explicar Genie (min 10-15)
3. Genie: explorar datos sin codigo, dashboards (min 15-33)
4. NB02: Assistant genera modelos ML con prompts (min 33-55)
5. NB03: cargar modelo + predecir perfiles (min 55-62)
6. HuggingFace app: audiencia interactua (min 62-65)
7. Cierre + reflexion (min 65-70)

## Problemas conocidos en Free Edition
- `mlflow.set_experiment()` causa error CONFIG_NOT_AVAILABLE. Usar `mlflow.start_run()` directo.
- `registered_model_name` en Unity Catalog da AccessDenied en S3. Solucion: `mlflow.set_registry_uri("databricks")` o variable `MLFLOW_USE_DATABRICKS_SDK_MODEL_ARTIFACTS_REPO_FOR_UC=True`.
- Import desde github.com bloqueado. Usar "Connect to a GitHub repo" en el setup wizard.
- El catalogo se llama "workspace", no "main".

## Repo
github.com/hebermudezg/masterclass-databricks

## App publica
huggingface.co/spaces/hebermudezg/unac
