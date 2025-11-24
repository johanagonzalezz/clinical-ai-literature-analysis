import networkx as nx
from collections import defaultdict
from agente_cfms.normalizer.normalizer import normalize_text


def to_key(value):
    """
    Convierte cualquier valor en una clave válida para diccionarios:
    - listas → "item1, item2"
    - None → ""
    - otros tipos → str()
    """
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def generar_taxonomia(grafo, registros, embeddings, clusters):
    """
    Genera una taxonomía clínica estructurada a partir de:
    - clusters semánticos
    - categorías del grafo
    - relaciones artículo → categoría
    """

    taxonomia = {
        "clusters": {},
        "dominios": defaultdict(list),
        "tareas": defaultdict(list),
        "arquitecturas": defaultdict(list),
        "tipos_datos": defaultdict(list),
        "limitaciones": defaultdict(list)
    }

    # =====================================
    # 1. AGRUPACIÓN POR CLUSTER
    # =====================================
    for idx, c in enumerate(clusters):
        cluster_id = int(c)

        if cluster_id not in taxonomia["clusters"]:
            taxonomia["clusters"][cluster_id] = {
                "articulos": [],
                "dominios": defaultdict(int),
                "tareas": defaultdict(int),
                "arquitecturas": defaultdict(int),
                "tipo_datos": defaultdict(int),
            }

        art = registros[idx]
        taxonomia["clusters"][cluster_id]["articulos"].append(art)

        # Normalizar claves
        dom = to_key(art.get("dominio_medico"))
        tar = to_key(art.get("tarea_principal"))
        arc = to_key(art.get("arquitectura_modelo"))
        tip = to_key(art.get("tipo_datos"))

        if dom:
            taxonomia["clusters"][cluster_id]["dominios"][dom] += 1
        if tar:
            taxonomia["clusters"][cluster_id]["tareas"][tar] += 1
        if arc:
            taxonomia["clusters"][cluster_id]["arquitecturas"][arc] += 1
        if tip:
            taxonomia["clusters"][cluster_id]["tipo_datos"][tip] += 1

    # =====================================
    # 2. ESTRUCTURA JERÁRQUICA GLOBAL
    # =====================================
    for art in registros:

        dom = to_key(art.get("dominio_medico"))
        tar = to_key(art.get("tarea_principal"))
        arc = to_key(art.get("arquitectura_modelo"))
        tip = to_key(art.get("tipo_datos"))

        if dom:
            taxonomia["dominios"][dom].append(art)

        if tar:
            taxonomia["tareas"][tar].append(art)

        if arc:
            taxonomia["arquitecturas"][arc].append(art)

        if tip:
            taxonomia["tipos_datos"][tip].append(art)

        # Limitaciones — lista
        for lim in art.get("limitaciones_reportadas", []):
            lim_key = to_key(lim)
            taxonomia["limitaciones"][lim_key].append(art)

    # =====================================
    # 3. TAXONOMÍA FINAL MULTINIVEL
    # =====================================

    estructura = {
        "Taxonomía Clínica CFMS": {
            "Dominios Clínicos": dict(taxonomia["dominios"]),
            "Tareas de IA": dict(taxonomia["tareas"]),
            "Arquitecturas de Modelo": dict(taxonomia["arquitecturas"]),
            "Tipos de Datos": dict(taxonomia["tipos_datos"]),
            "Limitaciones Reportadas": dict(taxonomia["limitaciones"]),
            "Clusters Semánticos": taxonomia["clusters"]
        }
    }

    return estructura

