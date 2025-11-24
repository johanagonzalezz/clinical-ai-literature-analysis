# -----------------------------------------------------------
# Configuración del extractor QWEN
# -----------------------------------------------------------

# Modelo LLM que usas para generar la estructura del artículo
MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

# Modelo de embeddings (Sentence Transformers)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Ruta al archivo CSV con tus artículos originales
CSV_PATH = "data/articulos_cfm.csv"

# Archivo donde se guardará el JSON estructurado con el output de QWEN
OUTPUT_JSON_PATH = "data/articulos_estructurados.json"

# Ruta donde se almacenará el grafo HTML interactivo generado por pyvis
GRAPH_HTML_PATH = "data/grafo_taxonomia.html"

