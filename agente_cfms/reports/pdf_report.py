from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_reporte_pdf(ruta_pdf, resumen_textual):
    styles = getSampleStyleSheet()
    estilo_normal = styles["Normal"]
    estilo_titulo = styles["Title"]

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)
    elementos = []

    elementos.append(Paragraph("Sistema de Extracción y Clasificación  de Artículos en Salud", estilo_titulo))
    elementos.append(Spacer(1, 20))

    for linea in resumen_textual.split("\n"):
        elementos.append(Paragraph(linea, estilo_normal))
        elementos.append(Spacer(1, 10))

    doc.build(elementos)
    print(f"[OK] Reporte clínico PDF guardado en: {ruta_pdf}")
