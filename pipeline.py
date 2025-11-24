"""
Pipeline completo:
1. Ejecuta extractor QWEN (estructura + embeddings + grafo HTML)
2. Copia JSON al agente CFMS
3. Ejecuta agente CFMS (clustering + grafos + taxonomía)
4. Genera visualizaciones y reporte final + PDF
"""

from qwen.run_qwen import run_qwen
from agente_cfms.main import main as run_cfms
from agente_cfms.reports.reporter import generar_reporte
from agente_cfms.reports.pdf_report import generar_reporte_pdf
import time


def pipeline_completo():
    print("\n====================================")
    print("   🚀 PIPELINE QWEN → CFMS INICIADO")
    print("====================================\n")

    inicio = time.time()

    # =============================
    # 1. EJECUTAR QWEN
    # =============================
    print("\n[1] Ejecutando agente QWEN...")
    registros = run_qwen()

    # =============================
    # 2. EJECUTAR AGENTE CFMS
    # =============================
    print("\n[2] Ejecutando agente CFMS...")
    taxonomia = run_cfms()

    # =============================
    # 3. REPORTE CLÍNICO
    # =============================
    print("\n[3] Generando reporte clínico...")
    reporte_textual = generar_reporte(taxonomia)

    # =============================
    # 4. PDF DEL REPORTE
    # =============================
    ruta_pdf = "agente_cfms/output/reporte_clinico.pdf"
    generar_reporte_pdf(ruta_pdf, reporte_textual)

    fin = time.time()

    print("\n====================================")
    print("   ✅ PIPELINE COMPLETO FINALIZADO")
    print(f"   Tiempo total: {fin - inicio:.2f} segundos")
    print("====================================\n")

    return taxonomia


if __name__ == "__main__":
    pipeline_completo()

