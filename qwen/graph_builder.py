import json
import networkx as nx
import torch
from torch.nn.functional import cosine_similarity
from .config import OUTPUT_JSON_PATH


def normalize_key(value: str):
    """Normaliza claves para evitar duplicación de nodos."""
    if not value:
        return None
    return (
        value.lower()
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def load_registros(path=OUTPUT_JSON_PATH):
    with open(path, "r", encoding="utf-8") as f:
        registros = json.load(f)
    return registros


def build_graph(registros: list, embeddings, sim_threshold: float = 0.6):
    G = nx.Graph()

    # ==========================
    # 1. NODOS DE ARTÍCULOS
    # ==========================
    for idx, reg in enumerate(registros):
        node_id = f"articulo_{idx}"

        G.add_node(
            node_id,
            tipo="articulo",
            titulo=reg.get("titulo", ""),
            arquitectura=reg.get("arquitectura_modelo"),
            tarea=reg.get("tarea_principal"),
            dominio=reg.get("dominio_medico"),
            label=reg.get("titulo", f"Artículo {idx}"),
            idx_embedding=idx,
        )

    # ==========================
    # 2. NODOS DE CATEGORÍAS
    # ==========================
    for reg in registros:
        # Arquitectura
        if reg.get("arquitectura_modelo"):
            key = normalize_key(reg["arquitectura_modelo"])
            if key:
                G.add_node(
                    f"arch_{key}",
                    tipo="arquitectura",
                    etiqueta=reg["arquitectura_modelo"],
                    label=f"Arquitectura: {reg['arquitectura_modelo']}",
                )

        # Tarea
        if reg.get("tarea_principal"):
            key = normalize_key(reg["tarea_principal"])
            if key:
                G.add_node(
                    f"tarea_{key}",
                    tipo="tarea",
                    etiqueta=reg["tarea_principal"],
                    label=f"Tarea: {reg['tarea_principal']}",
                )

        # Dominio
        if reg.get("dominio_medico"):
            key = normalize_key(reg["dominio_medico"])
            if key:
                G.add_node(
                    f"dom_{key}",
                    tipo="dominio",
                    etiqueta=reg["dominio_medico"],
                    label=f"Dominio: {reg['dominio_medico']}",
                )

    # ==========================
    # 3. ARISTAS artículo → categoría
    # ==========================
    for idx, reg in enumerate(registros):
        art_node = f"articulo_{idx}"

        if reg.get("arquitectura_modelo"):
            key = normalize_key(reg["arquitectura_modelo"])
            G.add_edge(art_node, f"arch_{key}")

        if reg.get("tarea_principal"):
            key = normalize_key(reg["tarea_principal"])
            G.add_edge(art_node, f"tarea_{key}")

        if reg.get("dominio_medico"):
            key = normalize_key(reg["dominio_medico"])
            G.add_edge(art_node, f"dom_{key}")

    # ==========================
    # 4. ARISTAS DE SIMILITUD ENTRE ARTÍCULOS
    # ==========================
    if embeddings is not None:
        emb = embeddings
        n = len(registros)

        for i in range(n):
            for j in range(i + 1, n):
                sim = cosine_similarity(
                    emb[i].unsqueeze(0), emb[j].unsqueeze(0)
                ).item()

                if sim >= sim_threshold:
                    G.add_edge(
                        f"articulo_{i}",
                        f"articulo_{j}",
                        tipo="similitud",
                        peso=sim,
                    )

    return G

