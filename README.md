# Pipeline de Análisis Semántico para Artículos de IA Clínica (CFMS)

Pipeline automatizado para el procesamiento, análisis de artículos científicos sobre inteligencia artificial aplicada al dominio clínico y médico.

## 📋 Descripción

Este proyecto implementa un pipeline completo que:
1. **Extrae** información estructurada de artículos científicos usando modelos de lenguaje (QWEN)
2. **Analiza** semánticamente el contenido mediante vectores de incrustación y agrupar datos similares entre sí sin necesidad de etiquetas.
3. **Genera** clasificaciones  del dominio clínico de IA
4. **Visualiza** los resultados mediante gráficos interactivos
5. **Produce** reportes en formato PDF

## 🏗️ Arquitectura

El pipeline está compuesto por dos agentes principales:

### 1. Agente QWEN
Extractor semántico basado en modelos de lenguaje que:
- Procesa artículos científicos en formato CSV
- Extrae entidades clínicas estructuradas (dominios médicos, tareas de IA, arquitecturas de modelos, etc.)
- Genera vectores de incrustación semánticos
- Construye visualizaciones HTML interactivos de los resultados

### 2. Agente CFMS
Motor de análisis y clasificació que incluye:
- **Loader**: Carga de datos estructurados en formato JSON
- **Normalizer**: Limpieza y poner los datos en un formato estándar,limpio y consistente de registros
- **Embeddings**: Generación de representaciones vectoriales semánticas
- **Analytics**: 
  - Cálculo de matrices de similitud
  - Agrupamiento de datos automático de artículos
- **Graph Builder**: Construcción de visualizaciones 
- **Taxonomy Engine**: Generación de clasificaciones clínicas por grupos
- **Reports**: 
  - Visualizaciones 
  - Reportes textuales
  - Generación de PDFs

## 📦 Estructura del Proyecto

```
cfms-pipeline-/
├── pipeline.py                    # Script principal del pipeline completo
├── requirements.txt               # Dependencias del proyecto
├── data/                         # Datos de entrada
│   ├── articulos_cfm.csv        # Artículos originales
│   ├── articulos_estructurados.json  # Datos procesados
│   └── grafo_taxonomia.html     # Visualización html
├── qwen/                         # Agente de extracción semántica
│   ├── run_qwen.py              # Ejecutor principal
│   ├── semantic_extractor.py    # Extractor de entidades
│   ├── graph_builder.py         # Constructor de visualizaciones
│   ├── visualize_graph.py       # Visualizador 
│   ├── prompts.py               # Prompts para el modelo
│   └── config.py                # Configuración
├── agente_cfms/                  # Agente de clasificación
│   ├── main.py                  # Punto de entrada del agente
│   ├── loader/                  # Cargadores de datos
│   │   └── json_loader.py
│   ├── normalizer/              # Homogenización de datos
│   │   └── normalizer.py
│   ├── embeddings/              # Generación de vectores de incrustación
│   │   └── semantic_extractor.py
│   ├── analytics/               # Análisis de similitud y agrupamiento
│   │   ├── similarity.py
│   │   └── clustering.py
│   ├── graph/                   # Construcción de vizualizaciones
│   │   └── graph_builder.py
│   ├── taxonomy/                # Generación de los resultados de clasificación
│   │   └── taxonomy_engine.py
│   ├── reports/                 # Generación de reportes
│   │   ├── reporter.py
│   │   ├── pdf_report.py
│   │   └── visualizations.py
│   ├── data/                    # Datos a procesar
│   └── output/                  # Resultados generados
│       ├── reporte_clinico.pdf
│       ├── taxonomia_cfms.json
│       ├── umap_clusters.png
│       ├── heatmap_similitud.png
│       └── grafo_cfms.png
└── lib/                         # Librerías de visualización
    ├── bindings/
    ├── tom-select/
    └── vis-9.1.2/
```

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd cfms-pipeline-
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

**Nota**: El archivo `requirements.txt` actual es mínimo. Las dependencias completas incluyen:
- `numpy`
- `pandas`
- `networkx`
- `scikit-learn`
- `matplotlib`
- `seaborn`
- `umap-learn`
- Librerías de modelos de lenguaje (según configuración QWEN)
- Librerías de generación de PDFs (reportlab o similar)

## 💻 Uso

### Ejecución del Pipeline Completo

Para ejecutar el pipeline completo desde la extracción hasta el reporte final:

```bash
python pipeline.py
```

Este comando ejecutará las siguientes etapas:
1. 🔍 Extracción con QWEN
2. 🧠 Análisis con agente CFMS
3. 📊 Generación de visualizaciones
4. 📄 Creación de reporte PDF

### Ejecución de Componentes Individuales

#### Solo el agente QWEN:
```bash
python -m qwen.run_qwen
```

#### Solo el agente CFMS:
```bash
python -m agente_cfms.main
```

## 📊 Clasificación Generada

El sistema genera una clasificación clínica multinivel que incluye:

- **Dominios Clínicos**: Áreas médicas (cardiología, neurología, radiología, etc.)
- **Tareas de IA**: Predicción, clasificación, segmentación, detección, etc.
- **Arquitecturas de Modelo**: Redes neuronales, transformers, modelos federados, etc.
- **Tipos de Datos**: ECG, EHR, imágenes médicas, señales biosensores, etc.
- **Limitaciones Reportadas**: Desafíos y restricciones identificados en los estudios
- **Patrones ocultos **: Agrupaciones automáticas de artículos similares

## 📈 Visualizaciones

El pipeline genera automáticamente:

1. **Visualiación de los resultados** (`grafo_taxonomia.html`): Visualización interactiva de las relaciones entre conceptos clínicos
2. **UMAP de agrupamiento** (`umap_clusters.png`): Proyección 2D de los embeddings mostrando los grupos identificados
3. **Heatmap de Similitud** (`heatmap_similitud.png`): Matriz de similitud entre artículos
4. **Red de los artículos** (`grafo_cfms.png`): Red de conocimiento de artículos relacionados

## 📝 Formato de Datos de Entrada

### Archivo CSV (`articulos_cfm.csv`)
Debe contener las siguientes columnas:
- `id_articulo`: Identificador único del artículo
- `titulo`: Título del artículo científico
- `abstract`: Resumen del artículo

### Archivo JSON Estructurado
Generado automáticamente por el agente QWEN, contiene:
- Información del artículo original
- Entidades extraídas:
  - `dominio_medico`
  - `tarea_principal`
  - `arquitectura_modelo`
  - `tipo_datos`
  - `limitaciones_reportadas`
- `Embeddings semánticos`

## 🔧 Configuración

La configuración del sistema se encuentra en:
- `qwen/config.py`: Configuración del modelo de extracción
- Variables de entorno o archivos de configuración adicionales según necesidad

## 📦 Salidas del Pipeline

El pipeline genera los siguientes archivos en `agente_cfms/output/`:

1. **taxonomia_cfms.json**: Clasificación completa en formato JSON
2. **reporte_clinico.pdf**: Reporte ejecutivo en formato PDF
3. **visualizaciones**: Gráficos PNG de análisis


## 📄 Licencia

MIT

*Nota**: Este pipeline está diseñado para investigación y análisis académico de literatura científica sobre IA en medicina. Los resultados deben ser interpretados en su contexto científico apropiado.
