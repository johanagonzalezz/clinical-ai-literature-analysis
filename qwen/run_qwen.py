import os
import json
import shutil
from .semantic_extractor import GenerativeTaxonomyAgent
from .graph_builder import build_graph
from .visualize_graph import visualize_graph
from .config import CSV_PATH, OUTPUT_JSON_PATH, GRAPH_HTML_PATH


def run_qwen():

    # ========================
    # Validación del CSV
    # ========================
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"No se encontró el archivo CSV en: {CSV_PATH}")

    agent = GenerativeTaxonomyAgent()

    # ========================
    # 1. Cargar artículos
    # ========================
    df = agent.load_articles(CSV_PATH)

    # ========================
    # 2. Estructurar info con Qwen 2.5
    # ========================
    registros = agent.process_corpus(df)

    # ========================
    # 3. Embeddings
    # ========================
    embeddings = agent.compute_embeddings(registros)

    # ========================
    # 4. Construcción del grafo
    # ========================
    G = build_graph(registros, embeddings, sim_threshold=0.6)

    # ========================
    # 5. Grafo interactivo HTML
    # ========================
    visualize_graph(G, output_path=GRAPH_HTML_PATH)

    # ========================
    # 6. Guardar JSON del extractor
    # ========================
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)

    print(f"[OK] JSON creado en: {OUTPUT_JSON_PATH}")

    # ========================
    # 7. Copiar JSON hacia CFMS
    # ========================
    os.makedirs("agente_cfms/data", exist_ok=True)

    shutil.copy(
        OUTPUT_JSON_PATH,
        "agente_cfms/data/articulos_estructurados.json"
    )

    print("[OK] JSON copiado a agente_cfms/data/articulos_estructurados.json")

    return registros


if __name__ == "__main__":
    run_qwen()

