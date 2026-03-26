# Master Class: Analisis de Datos en Databricks con IA

## Info
- **Fecha:** 16 de abril de 2026, 7:00 PM
- **Duracion:** 1.5 - 2 horas
- **Formato:** Demo en vivo (tu presentas, ellos observan)
- **Plataforma:** Databricks Community Edition + Streamlit Cloud

## Caso: Cafe Origen
Cadena de cafeterias colombiana, 5 sucursales, ~4,700 ventas.
La gerente (Dona Marta) necesita datos para decidir si abre una 6ta sucursal.

## Estructura de la Sesion
| # | Bloque | Min | Que pasa |
|---|--------|-----|----------|
| 1 | Intro | 10 | Contexto: "Dona Marta nos contrato" |
| 2 | Setup | 15 | Cargar datos en Databricks |
| 3 | Exploracion | 25 | EDA con Databricks Assistant (IA) |
| 4 | Analisis | 25 | Preguntas de negocio |
| 5 | Visualizacion | 20 | Graficos en Databricks |
| 6 | Deploy | 15 | Mostrar dashboard en Streamlit (URL publica) |
| 7 | Cierre | 10 | Conclusiones y compartir material |

## Estructura de Carpetas
```
masterclass-databricks/
├── README.md
├── dataset/                        ← CSVs para subir a Databricks
│   ├── ventas.csv
│   ├── productos.csv
│   └── sucursales.csv
├── notebooks/                      ← Importar en Databricks
│   ├── 00_setup.py
│   ├── 01_exploracion.py
│   ├── 02_transformaciones.py
│   └── 03_visualizacion.py
├── streamlit-app/                  ← Dashboard desplegable
│   ├── app.py
│   ├── requirements.txt
│   ├── DEPLOY.md
│   ├── .streamlit/config.toml
│   └── data/
│       ├── ventas.csv
│       ├── productos.csv
│       └── sucursales.csv
└── presentacion/
    └── guia_masterclass.md         ← Guion completo paso a paso
```

## Deploy rapido del dashboard
```bash
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py
```
Para desplegar en la nube gratis, ver `streamlit-app/DEPLOY.md`
