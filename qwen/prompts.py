SYSTEM_PROMPT = (
    "You are an expert biomedical information extraction system. "
    "Given an abstract, extract key structured elements. "
    "Always return ONLY a valid JSON object."
)

USER_PROMPT_TEMPLATE = """
Extract the following fields from the abstract:

- arquitectura_modelo
- tarea_principal
- dominio_medico
- tipo_datos
- recursos_datos
- limitaciones_reportadas
- comentarios_relevantes

Abstract:
{abstract}

Return ONLY JSON.
"""

