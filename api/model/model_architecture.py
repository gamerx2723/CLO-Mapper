"""
Neural Network Architecture for OBE Cognitive Classification and CLO Alignment
Dual-Head Architecture:
- Head 1: Bloom's Taxonomy Cognitive Demand (Levels 1, 2, 3)
- Head 2: Semantic Metric Projector (L2-normalized embedding for cosine similarity)
"""

import math
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
    _BaseModule = nn.Module
except ImportError:
    TORCH_AVAILABLE = False
    _BaseModule = object

class OBECognitiveNeuralNetwork(_BaseModule):
    def __init__(self, vocab_size: int, embed_dim: int = 128, hidden_dim: int = 64, proj_dim: int = 64):
        super(OBECognitiveNeuralNetwork, self).__init__()
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.proj_dim = proj_dim

        self.fc1 = nn.Linear(vocab_size, embed_dim)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.dropout1 = nn.Dropout(0.15)

        self.fc2 = nn.Linear(embed_dim, hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.activation = nn.Mish()

        self.cognitive_head = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.Mish(),
            nn.Dropout(0.1),
            nn.Linear(32, 3)
        )

        self.semantic_projector = nn.Sequential(
            nn.Linear(hidden_dim, proj_dim),
            nn.Mish(),
            nn.Linear(proj_dim, proj_dim)
        )

    def forward(self, x: torch.Tensor):
        h = self.fc1(x)
        h = self.norm1(h)
        h = self.activation(h)
        h = self.dropout1(h)

        h2 = self.fc2(h)
        h2 = self.norm2(h2)
        h2 = self.activation(h2)

        cognitive_logits = self.cognitive_head(h2)
        semantic_emb = self.semantic_projector(h2)
        semantic_emb = F.normalize(semantic_emb, p=2, dim=1)

        return cognitive_logits, semantic_emb

    def export_numpy_weights(self) -> dict:
        weights = {}
        for name, param in self.named_parameters():
            weights[name] = param.detach().cpu().numpy().tolist()
        return {
            "vocab_size": self.vocab_size,
            "embed_dim": self.embed_dim,
            "hidden_dim": self.hidden_dim,
            "proj_dim": self.proj_dim,
            "weights": weights
        }


class FastNumPyInference:
    def __init__(self, export_dict: dict):
        self.vocab_size = export_dict["vocab_size"]
        self.weights = {k: np.array(v, dtype=np.float32) for k, v in export_dict["weights"].items()}

    def _mish(self, x):
        return x * np.tanh(np.log1p(np.exp(np.clip(x, -20, 20))))

    def _layer_norm(self, x, weight, bias, eps=1e-5):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return (x - mean) / np.sqrt(var + eps) * weight + bias

    def _softmax(self, x, axis=-1):
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def forward(self, x: np.ndarray):
        w_fc1 = self.weights["fc1.weight"]
        b_fc1 = self.weights["fc1.bias"]
        h = np.dot(x, w_fc1.T) + b_fc1
        h = self._layer_norm(h, self.weights["norm1.weight"], self.weights["norm1.bias"])
        h = self._mish(h)

        w_fc2 = self.weights["fc2.weight"]
        b_fc2 = self.weights["fc2.bias"]
        h2 = np.dot(h, w_fc2.T) + b_fc2
        h2 = self._layer_norm(h2, self.weights["norm2.weight"], self.weights["norm2.bias"])
        h2 = self._mish(h2)

        w_c1 = self.weights["cognitive_head.0.weight"]
        b_c1 = self.weights["cognitive_head.0.bias"]
        c1 = self._mish(np.dot(h2, w_c1.T) + b_c1)
        w_c2 = self.weights["cognitive_head.3.weight"]
        b_c2 = self.weights["cognitive_head.3.bias"]
        cog_logits = np.dot(c1, w_c2.T) + b_c2
        cog_probs = self._softmax(cog_logits)

        w_p1 = self.weights["semantic_projector.0.weight"]
        b_p1 = self.weights["semantic_projector.0.bias"]
        p1 = self._mish(np.dot(h2, w_p1.T) + b_p1)
        w_p2 = self.weights["semantic_projector.2.weight"]
        b_p2 = self.weights["semantic_projector.2.bias"]
        sem_emb = np.dot(p1, w_p2.T) + b_p2
        norm = np.linalg.norm(sem_emb, axis=-1, keepdims=True) + 1e-9
        sem_emb = sem_emb / norm

        return cog_probs, sem_emb
