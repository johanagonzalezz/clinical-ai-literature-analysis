from agente_cfms.loader.json_loader import cargar_json
from agente_cfms.normalizer.normalizer import limpiar_registro
from agente_cfms.embeddings.semantic_extractor import compute_embeddings
from agente_cfms.analytics.similarity import matriz_similitud
from agente_cfms.analytics.clustering import clusterizar
from agente_cfms.graph.graph_builder import construir_grafo
from agente_cfms.taxonomy.taxonomy_engine import generar_taxonomia

from agente_cfms.reports.reporter import exportar_json
from agente_cfms.reports.visualizations import plot_umap, plot_heatmap, plot_grafo


def main():
    print("Cargando artículos...")

    registros_raw = cargar_json("data/articulos_estructurados.json")
    registros = [limpiar_registro(r) for r in registros_raw]

    print("Generando embeddings...")
    embeddings = compute_embeddings(registros)

    print("Calculando similitud...")
    sim = matriz_similitud(embeddings)

    print("Clusterizando...")
    clusters = clusterizar(embeddings)

    print("Construyendo grafo...")
    grafo = construir_grafo(registros, embeddings, sim)

    print("Generando taxonomía...")
    taxonomia = generar_taxonomia(grafo, registros, embeddings, clusters)

    print("Exportando resultados...")
    exportar_json(taxonomia)

    print("Generando visualizaciones...")
    plot_umap(embeddings, clusters)
    plot_heatmap(sim)
    plot_grafo(grafo)

    print("¡Proceso completo!")
    return taxonomia


if __name__ == '__main__':
    main()

