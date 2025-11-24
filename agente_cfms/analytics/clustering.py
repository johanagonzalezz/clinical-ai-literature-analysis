import hdbscan
import numpy as np

def clusterizar(embeddings, min_cluster_size=3, min_samples=1):
    """
    Clustering para embeddings semánticos usando HDBSCAN.
    - No requiere elegir k.
    - Detecta outliers.
    - Produce clusters coherentes para taxonomía.
    """
    clusterer = hdbscan.HDBSCAN(
        metric='euclidean',
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        cluster_selection_method='eom'
    )

    etiquetas = clusterer.fit_predict(embeddings)

    return etiquetas

