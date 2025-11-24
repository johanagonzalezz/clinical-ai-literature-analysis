import json
import os

# Carpeta de salida estándar
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================
# 1. EXPORTAR JSON
# ============================================
def exportar_json(taxonomia, filename="taxonomia_cfms.json"):
    """
    Exporta la taxonomía final CFMS en formato JSON.
    """
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(taxonomia, f, ensure_ascii=False, indent=4)
    print(f"[OK] Taxonomía en JSON guardada en: {path}")


# ============================================
# 2. REPORTE CLÍNICO (texto para consola + PDF)
# ============================================
def generar_reporte(taxonomia):
    """
    Imprime en consola y también retorna el texto completo
    para poder guardarlo en PDF.
    """

    texto = ""  # acumulador para PDF

    def add(linea):
        nonlocal texto
        print(linea)
        texto += linea + "\n"

    add("\n=== 📘 TAXONOMÍA CLÍNICA CFMS ===\n")

    t = taxonomia.get("Taxonomía Clínica CFMS", {})

    # -----------------------------
    # DOMINIOS
    # -----------------------------
    add("🔵 DOMINIOS CLÍNICOS")
    for dom, arts in t.get("Dominios Clínicos", {}).items():
        add(f" - {dom}: {len(arts)} artículos")

    # -----------------------------
    # TAREAS
    # -----------------------------
    add("\n🟠 TAREAS DE IA")
    for tar, arts in t.get("Tareas de IA", {}).items():
        add(f" - {tar}: {len(arts)} artículos")

    # -----------------------------
    # ARQUITECTURAS
    # -----------------------------
    add("\n🟢 ARQUITECTURAS DE MODELO")
    for arc, arts in t.get("Arquitecturas de Modelo", {}).items():
        add(f" - {arc}: {len(arts)} artículos")

    # -----------------------------
    # TIPOS DE DATOS
    # -----------------------------
    add("\n🟣 TIPOS DE DATOS")
    for tip, arts in t.get("Tipos de Datos", {}).items():
        add(f" - {tip}: {len(arts)} artículos")

    # -----------------------------
    # LIMITACIONES
    # -----------------------------
    add("\n🔴 LIMITACIONES REPORTADAS")
    for lim, arts in t.get("Limitaciones Reportadas", {}).items():
        add(f" - {lim}: {len(arts)} artículos")

    # -----------------------------
    # CLUSTERS
    # -----------------------------
    add("\n⚡ CLUSTERS SEMÁNTICOS")
    for cid, datos in t.get("Clusters Semánticos", {}).items():
        add(f" - Cluster {cid}: {len(datos['articulos'])} artículos")

    add("\n=== FIN DEL REPORTE ===\n")

    # Retornar el texto para el PDF
    return texto


# ============================================
# 3. EXPORTAR PDF
# ============================================
def exportar_pdf(texto, filename="taxonomia_cfms.pdf"):
    """
    Exportación simple a PDF usando reportlab.
    """
    try:
        from reportlab.pdfgen import canvas
    except ImportError:
        print("[WARN] reportlab no instalado. Instala con: pip install reportlab")
        return

    path = os.path.join(OUTPUT_DIR, filename)
    c = canvas.Canvas(path)
    y = 800

    for linea in texto.split("\n"):
        c.drawString(40, y, linea)
        y -= 15

        if y < 40:   # salto de página automático
            c.showPage()
            y = 800

    c.save()
    print(f"[OK] PDF guardado en: {path}")

