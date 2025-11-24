import os
import numpy as np
import umap
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors


OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)



# ============================================
# 1. UMAP CON CLUSTERS (COMPATIBLE CON HDBSCAN)
# ============================================
def plot_umap(embeddings, clusters, filename="umap_clusters.png"):
    print("[INFO] Generando UMAP...")

    reducer = umap.UMAP(random_state=42)
    emb_2d = reducer.fit_transform(embeddings)

    plt.figure(figsize=(8, 6))

    # Convertir clusters -1 → 0 (ruido)
    cluster_labels = np.array(clusters)
    unique_clusters = np.unique(cluster_labels)

    # Colormap discreto
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_clusters)))

    for idx, cl in enumerate(unique_clusters):
        mask = cluster_labels == cl
        label = f"Cluster {cl}" if cl != -1 else "Ruido (-1)"

        plt.scatter(
            emb_2d[mask, 0],
            emb_2d[mask, 1],
            s=40,
            color=colors[idx],
            label=label,
            alpha=0.8,
        )

    plt.title("UMAP - Clusters de Artículos")
    plt.legend()
    plt.xlabel("Dim 1")
    plt.ylabel("Dim 2")

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"[OK] Gráfico UMAP guardado en: {path}")



# ============================================
# 2. HEATMAP DE SIMILITUD SIN SEABORN
# ============================================
def plot_heatmap(sim_matrix, filename="heatmap_similitud.png"):
    print("[INFO] Generando heatmap de similitud...")

    plt.figure(figsize=(10, 8))
    plt.imshow(sim_matrix, cmap="viridis", aspect="auto")
    plt.colorbar(label="Similitud")
    plt.title("Matriz de Similitud")
    plt.xlabel("Artículo")
    plt.ylabel("Artículo")

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"[OK] Heatmap guardado en: {path}")



# ============================================
# 3. GRAFO — AVISO IMPORTANTE
# ============================================
def plot_grafo(grafo, filename="grafo_cfms.png"):
    """
    Este método genera un gráfico estático MUY limitado.
    El grafo REAL se debe visualizar con PyVis (HTML interactivo).

    Se deja este método solo para diagnóstico rápido.
    """

    print("[ADVERTENCIA] Se recomienda usar PyVis para una visualización profesional del grafo.")

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(grafo, seed=42)

    # Colores por tipo de nodo
    color_map = []
    for _, data in grafo.nodes(data=True):
        tipo = data.get("tipo", "articulo")
        if tipo == "articulo":
            color_map.append("skyblue")
        elif tipo == "arquitectura":
            color_map.append("green")
        elif tipo == "tarea":
            color_map.append("orange")
        elif tipo == "dominio":
            color_map.append("red")
        elif tipo == "tipo_datos":
            color_map.append("purple")
        else:
            color_map.append("gray")

    nx.draw(
        grafo,
        pos,
        node_color=color_map,
        with_labels=False,
        node_size=200,
        alpha=0.8
    )

    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=200)
    plt.close()
    print(f"[OK] Grafo estático guardado en: {path}")

