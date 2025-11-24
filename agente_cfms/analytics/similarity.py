
import numpy as np

def matriz_similitud(emb):
    norm = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-10)
    return np.dot(norm, norm.T)
