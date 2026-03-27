# Master Class: Analisis de Datos en Databricks con IA

## Info
- **Fecha:** 16 de abril de 2026, 7:00 PM
- **Duracion:** 1.5 - 2 horas
- **Formato:** Demo en vivo (presentador conduce, audiencia observa)
- **Plataforma:** Databricks Trial Premium (14 dias gratis)

## Caso: Cafe Origen
Cadena de cafeterias colombiana, 5 sucursales, ~4,700 ventas.
La gerente (Dona Marta) necesita datos para decidir si abre una 6ta sucursal.

## Estructura de la Sesion
| # | Bloque | Min | Que pasa |
|---|--------|-----|----------|
| 1 | Intro | 10 | "Dona Marta nos contrato" |
| 2 | Setup | 15 | Cargar datos en Databricks |
| 3 | Exploracion | 25 | EDA con Databricks Assistant (IA genera codigo) |
| 4 | Analisis | 25 | Preguntas de negocio |
| 5 | Dashboard | 20 | SQL Dashboard nativo con URL compartible |
| 6 | Genie | 15 | IA responde preguntas en lenguaje natural |
| 7 | Cierre | 10 | Conclusiones y material |

## Estructura de Carpetas
```
masterclass-databricks/
├── README.md
├── dataset/                           <- CSVs para subir a Databricks
│   ├── ventas.csv                        (~4,700 transacciones)
│   ├── productos.csv                     (20 productos)
│   └── sucursales.csv                    (5 sucursales)
├── notebooks/                         <- Importar en Databricks
│   ├── 00_setup.py                       Cargar datos
│   ├── 01_exploracion.py                 EDA con IA
│   ├── 02_transformaciones.py            Analisis de negocio
│   ├── 03_visualizacion.py               Graficos en notebook
│   └── 04_sql_dashboard.py              Tablas + Dashboard + Genie
├── presentacion/
│   ├── guia_masterclass.md            <- Guion paso a paso
│   └── guia_trial_databricks.md       <- Como activar el trial gratis
└── streamlit-app/                     <- Plan B: dashboard Streamlit
    ├── app.py
    ├── requirements.txt
    └── data/
```

## Quick Start
1. Activar trial de Databricks (ver `presentacion/guia_trial_databricks.md`)
2. Subir los 3 CSVs de `dataset/`
3. Importar los 5 notebooks de `notebooks/`
4. Ejecutar en orden: 00 -> 01 -> 02 -> 03 -> 04
5. Crear SQL Dashboard y Genie Space (instrucciones en notebook 04)
