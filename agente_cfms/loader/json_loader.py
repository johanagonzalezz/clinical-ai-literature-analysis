import json
import os

# Directorio base del módulo agente_cfms
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def cargar_json(path):
    """
    Carga un archivo JSON usando una ruta relativa desde el root de agente_cfms.

    Ejemplo esperado de path:
    "data/articulos_estructurados.json"
    """
    full = os.path.join(BASE_DIR, path)

    if not os.path.exists(full):
        raise FileNotFoundError(f"No se encontró el archivo JSON en: {full}")

    with open(full, "r", encoding="utf-8") as f:
        return json.load(f)

