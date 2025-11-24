import re

def normalize_text(x: str):
    """Limpieza básica: lowercase, quitar espacios extra, normalizar caracteres."""
    if not isinstance(x, str):
        return x
    x = x.lower().strip()
    x = re.sub(r"\s+", " ", x)
    return x


def normalize_list(v):
    """Normaliza listas preservando estructura."""
    if not isinstance(v, list):
        return v
    cleaned = []
    for item in v:
        if isinstance(item, dict):
            cleaned.append(normalize_dict(item))
        elif isinstance(item, list):
            cleaned.append(normalize_list(item))
        else:
            cleaned.append(normalize_text(item))
    return cleaned


def normalize_dict(d):
    """Normaliza diccionarios sin destruir la estructura."""
    if not isinstance(d, dict):
        return d
    result = {}
    for k, v in d.items():
        if isinstance(v, list):
            result[k] = normalize_list(v)
        elif isinstance(v, dict):
            result[k] = normalize_dict(v)
        else:
            result[k] = normalize_text(v)
    return result


def limpiar_registro(registro):
    """
    Normaliza SOLO los campos relevantes para embeddings y grafo.
    Preserva la estructura original del JSON, evita convertir todo a texto.
    """
    campos_relevantes = [
        "titulo",
        "id_articulo",
        "arquitectura_modelo",
        "tarea_principal",
        "dominio_medico",
        "tipo_datos",
        "recursos_datos",
        "limitaciones_reportadas",
        "comentarios_relevantes",
    ]

    limpio = {}
    for key in campos_relevantes:
        if key in registro:
            val = registro[key]
            if isinstance(val, list):
                limpio[key] = normalize_list(val)
            elif isinstance(val, dict):
                limpio[key] = normalize_dict(val)
            else:
                limpio[key] = normalize_text(val)

    return limpio

