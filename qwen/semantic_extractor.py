import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from sentence_transformers import SentenceTransformer
from .config import MODEL_NAME, EMBEDDING_MODEL, CSV_PATH, OUTPUT_JSON_PATH
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE


def normalizar_valor(v):
    """Convierte cualquier valor en una cadena segura para embeddings."""
    if v is None:
        return ""
    if isinstance(v, list):
        return " | ".join(normalizar_valor(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}: {normalizar_valor(v2)}" for k, v2 in v.items())
    return str(v)


class GenerativeTaxonomyAgent:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        print(f"Cargando modelo Qwen2.5 Instruct en {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32,
        ).to(self.device)

        print("Cargando modelo de embeddings...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL, device=self.device)

    def load_articles(self, csv_path=CSV_PATH):
        df = pd.read_csv(csv_path)
        print(f"Se cargaron {len(df)} artículos desde {csv_path}")
        return df

    def _build_prompt(self, abstract: str) -> str:
        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"Abstract:\n{abstract}\n\n"
            "Return ONLY valid JSON with this structure:\n"
            "{\n"
            "  \"arquitectura_modelo\": \"...\",\n"
            "  \"tarea_principal\": \"...\",\n"
            "  \"dominio_medico\": \"...\",\n"
            "  \"tipo_datos\": \"...\",\n"
            "  \"recursos_datos\": \"...\",\n"
            "  \"limitaciones_reportadas\": [\"...\"],\n"
            "  \"comentarios_relevantes\": \"...\"\n"
            "}\n"
        )

    def _generate_json_from_abstract(self, abstract: str) -> dict:
        prompt = self._build_prompt(abstract)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.0,
            do_sample=False
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        json_str = self._extract_json_block(decoded)

        try:
            data = json.loads(json_str)
        except:
            print("⚠ JSON inválido. Usando estructura vacía.")
            data = {
                "arquitectura_modelo": None,
                "tarea_principal": None,
                "dominio_medico": None,
                "tipo_datos": None,
                "recursos_datos": None,
                "limitaciones_reportadas": [],
                "comentarios_relevantes": "",
            }

        return data

    @staticmethod
    def _extract_json_block(text: str) -> str:
        """Extrae el bloque JSON más grande válido dentro del texto."""
        import re
        import json

        # Buscar bloques tipo ```json { ... } ```
        code_blocks = re.findall(r"```json(.*?)```", text, re.DOTALL | re.IGNORECASE)
        for block in code_blocks:
            try:
                json.loads(block.strip())
                return block.strip()
            except:
                pass

        # Buscar bloques {...}
        brace_blocks = re.findall(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", text, re.DOTALL)

        valid = []
        for block in brace_blocks:
            try:
                json.loads(block)
                valid.append(block)
            except:
                pass

        if valid:
            return max(valid, key=len)

        return "{}"

    def process_corpus(self, df):
        registros = []

        print(f"Procesando {len(df)} artículos...")

        for _, row in df.iterrows():
            titulo = row.get("titulo", "sin título")
            abstract = row.get("abstract", "")

            print(f"\nProcesando artículo: {titulo}")

            info = self._generate_json_from_abstract(abstract)

            # === MUY IMPORTANTE: tus columnas reales ==
            info["id_articulo"] = row.get("id_articulo", None)
            info["titulo"] = titulo

            registros.append(info)

        with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=2)

        print(f"\nJSON generado en: {OUTPUT_JSON_PATH}")
        return registros

    def compute_embeddings(self, registros):
        textos = []
        for r in registros:
            partes = [
                r.get("arquitectura_modelo") or "",
                r.get("tarea_principal") or "",
                r.get("dominio_medico") or "",
                r.get("tipo_datos") or "",
                r.get("comentarios_relevantes") or "",
                " ".join(r.get("limitaciones_reportadas") or []),
                r.get("recursos_datos") or "",
            ]

            partes_normalizadas = [normalizar_valor(p) for p in partes]
            textos.append(" | ".join(partes_normalizadas))

        embeddings = self.embedding_model.encode(textos, convert_to_tensor=True)
        print("Embeddings generados correctamente.")
        return embeddings

