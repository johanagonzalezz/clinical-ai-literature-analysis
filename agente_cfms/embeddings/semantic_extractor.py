from sentence_transformers import SentenceTransformer
from agente_cfms.normalizer.normalizer import normalize_text
import numpy as np

# Modelo recomendado (mismo que en QWEN)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Cargar una sola vez
_embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def compute_embeddings(registros):
    """
    Genera embeddings reales usando Sentence Transformers.
    Compatible con campos tipo lista, string o None.
    """

    def to_text(value):
        """
        Convierte cualquier valor a texto seguro:
        - listas → "item1, item2"
        - None → ""
        - números → str()
        - strings → se regresan igual
        """
        if value is None:
            return ""
        if isinstance(value, list):
            return ", ".join(str(v) for v in value)
        return str(value)

    textos = []
    
    for r in registros:
        partes = [
            to_text(r.get("titulo", "")),
            to_text(r.get("arquitectura_modelo", "")),
            to_text(r.get("tarea_principal", "")),
            to_text(r.get("dominio_medico", "")),
            to_text(r.get("tipo_datos", "")),
            to_text(r.get("comentarios_relevantes", "")),
            to_text(r.get("limitaciones_reportadas", [])),
            to_text(r.get("recursos_datos", "")),
        ]

        texto = " | ".join(normalize_text(p) for p in partes)
        textos.append(texto)

    # Embeddings reales — no se modifica
    embeddings = _embedding_model.encode(
        textos,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings

