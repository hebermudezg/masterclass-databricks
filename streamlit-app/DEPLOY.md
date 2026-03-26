# Desplegar el Dashboard en Streamlit Community Cloud (GRATIS)

## Paso 1: Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `cafe-origen-dashboard`
3. Público
4. Sube TODO el contenido de la carpeta `streamlit-app/`:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml`
   - `data/ventas.csv`
   - `data/productos.csv`
   - `data/sucursales.csv`

## Paso 2: Desplegar en Streamlit Cloud
1. Ve a https://share.streamlit.io/
2. Inicia sesión con tu cuenta de GitHub
3. Click en "New app"
4. Selecciona tu repositorio `cafe-origen-dashboard`
5. Branch: `main`
6. Main file path: `app.py`
7. Click en "Deploy"

## Paso 3: Listo!
En ~2 minutos tendrás una URL pública tipo:
`https://cafe-origen-dashboard.streamlit.app`

Cualquier persona con el link puede ver el dashboard.
No requiere cuenta ni instalación.

## Probar en local antes de desplegar
```bash
cd streamlit-app
pip install -r requirements.txt
streamlit run app.py
```
Se abre en http://localhost:8501

## Notas
- Streamlit Community Cloud es 100% gratis
- La app se "duerme" después de unos días sin visitas, pero se reactiva al entrar
- Se actualiza automáticamente cuando haces push al repo
