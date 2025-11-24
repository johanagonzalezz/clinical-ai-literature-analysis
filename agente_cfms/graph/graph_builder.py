import networkx as nx
from agente_cfms.normalizer.normalizer import normalize_text, normalize_list


def construir_grafo(registros, embeddings, sim_matrix, sim_threshold=0.75):
    """
    Construye un grafo semántico clínico completo para CFMS.
    - Incluye nodos de artículos
    - Incluye nodos de categorías
    - Crea aristas semánticas
    - Crea aristas por similitud
    """

    G = nx.Graph()

    # ============================================
    # 1. NODOS DE ARTÍCULOS
    # ============================================
    for i, r in enumerate(registros):
        G.add_node(
            f"art_{i}",
            tipo="articulo",
            titulo=r.get("titulo", f"Artículo {i}"),
            arquitectura=r.get("arquitectura_modelo"),
            tarea=r.get("tarea_principal"),
            dominio=r.get("dominio_medico"),
            tipo_datos=r.get("tipo_datos"),
            limitaciones=r.get("limitaciones_reportadas"),
            recursos=r.get("recursos_datos"),
        )

    # ============================================
    # 2. NODOS DE CATEGORÍAS (arquitectura, tarea, dominio, etc.)
    # ============================================

    def add_category_node(prefix, value):
        if not value:
            return None
        key = normalize_text(str(value)).replace(" ", "_")
        node_id = f"{prefix}_{key}"
        if node_id not in G:
            G.add_node(
                node_id,
                tipo=prefix,
                etiqueta=value
            )
        return node_id

    # ============================================
    # 3. ARISTAS DE ARTÍCULO → CATEGORÍA
    # ============================================
    for i, r in enumerate(registros):

        art_node = f"art_{i}"

        # Arquitectura
        nodo_arch = add_category_node("arquitectura", r.get("arquitectura_modelo"))
        if nodo_arch:
            G.add_edge(art_node, nodo_arch)

        # Tarea
        nodo_tarea = add_category_node("tarea", r.get("tarea_principal"))
        if nodo_tarea:
            G.add_edge(art_node, nodo_tarea)

        # Dominio
        nodo_dom = add_category_node("dominio", r.get("dominio_medico"))
        if nodo_dom:
            G.add_edge(art_node, nodo_dom)

        # Tipo de datos
        nodo_tipo = add_category_node("tipo_datos", r.get("tipo_datos"))
        if nodo_tipo:
            G.add_edge(art_node, nodo_tipo)

        # Recursos de datos
        nodo_recurso = add_category_node("recurso_datos", r.get("recursos_datos"))
        if nodo_recurso:
            G.add_edge(art_node, nodo_recurso)

        # Limitaciones → nodos múltiples
        if isinstance(r.get("limitaciones_reportadas"), list):
            for lim in r["limitaciones_reportadas"]:
                nodo_lim = add_category_node("limitacion", lim)
                if nodo_lim:
                    G.add_edge(art_node, nodo_lim)

    # ============================================
    # 4. ARISTAS DE SIMILITUD ENTRE ARTÍCULOS
    # ============================================
    n = len(registros)
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i][j] >= sim_threshold:
                G.add_edge(
                    f"art_{i}",
                    f"art_{j}",
                    tipo="similitud",
                    peso=float(sim_matrix[i][j]),
                )

    return G

