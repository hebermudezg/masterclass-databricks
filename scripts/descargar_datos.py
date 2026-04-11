"""
Descarga resultados del ICFES Saber 11 desde datos.gov.co

Dataset: Resultados Unicos Saber 11 (ID: kgxf-xxbe)
Fuente: https://www.datos.gov.co/d/kgxf-xxbe
Registros totales: 7,109,704
"""

import os
import urllib.request

# Descarga filtrada via API SODA (50K filas, periodos 2020+, con puntaje)
URL_FILTRADA = (
    "https://www.datos.gov.co/resource/kgxf-xxbe.csv"
    "?$limit=50000"
    "&$where=punt_global%20IS%20NOT%20NULL%20AND%20periodo%20%3E=%20%2720201%27"
    "&$order=periodo%20DESC"
)

# Descarga completa (7M+ filas, ~500MB)
URL_COMPLETA = (
    "https://www.datos.gov.co/api/views/kgxf-xxbe/rows.csv?accessType=DOWNLOAD"
)

DESTINO = os.path.join(os.path.dirname(__file__), "..", "data", "icfes_saber11.csv")


def descargar(completa=False):
    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    url = URL_COMPLETA if completa else URL_FILTRADA
    modo = "completa (7M+ filas)" if completa else "filtrada (50K filas, 2020+)"
    print(f"Descargando dataset ICFES Saber 11 ({modo})...")
    urllib.request.urlretrieve(url, DESTINO)
    size_mb = os.path.getsize(DESTINO) / (1024 * 1024)
    print(f"Descarga completada: {DESTINO} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    descargar()
