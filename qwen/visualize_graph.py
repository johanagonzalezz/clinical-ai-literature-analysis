from pyvis.network import Network
import networkx as nx
from .config import GRAPH_HTML_PATH


def visualize_graph(G: nx.Graph, output_path=GRAPH_HTML_PATH):
    """
    Visualiza un grafo NetworkX con PyVis, usando labels y tooltips enriquecidos.
    """
    net = Network(height="750px", width="100%", notebook=False, directed=False)
    net.toggle_physics(True)

    # ==========================
    # 1. Agregar nodos
    # ==========================
    for node, data in G.nodes(data=True):

        tipo = data.get("tipo", "articulo")

        # Usa la etiqueta ya preparada en graph_builder.py
        label = data.get("label", node)

        # Construcción del tooltip enriquecido
        tooltip = f"<b>{label}</b>"
        if tipo == "articulo":
            tooltip += (
                f"<br><b>Arquitectura:</b> {data.get('arquitectura')}"
                f"<br><b>Tarea:</b> {data.get('tarea')}"
                f"<br><b>Dominio:</b> {data.get('dominio')}"
            )
        else:
            tooltip += f"<br><i>{tipo.capitalize()}</i>"

        # Colores por tipo
        if tipo == "articulo":
            color = "#1f77b4"
            shape = "dot"
        elif tipo == "arquitectura":
            color = "#2ca02c"
            shape = "diamond"
        elif tipo == "tarea":
            color = "#ff7f0e"
            shape = "triangle"
        elif tipo == "dominio":
            color = "#d62728"
            shape = "square"
        else:
            color = "#7f7f7f"
            shape = "dot"

        net.add_node(
            node,
            label=label,
            title=tooltip,
            color=color,
            shape=shape,
        )

    # ==========================
    # 2. Agregar aristas
    # ==========================
    for u, v, data in G.edges(data=True):
        edge_title = ""

        if data.get("tipo") == "similitud":
            edge_title = f"Similitud: {data.get('peso', 0):.2f}"

        net.add_edge(u, v, title=edge_title)

    # ==========================
    # 3. Exportar HTML
    # ==========================
    net.write_html(output_path)
    print(f"Grafo interactivo guardado en: {output_path}")

