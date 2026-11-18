"""
Local OBE Cognitive Alignment Inference Engine
Zero API Keys | 100% Offline | Sub-millisecond Neural Inference
"""

import os
import re
import json
import numpy as np
from typing import List, Dict, Any

from model.dataset import BLOOM_VERB_MAP
from model.model_architecture import FastNumPyInference

BLOOM_TIER_MAPPING = {
    "c1": 0, "knowledge": 0, "remember": 0,
    "c2": 0, "comprehension": 0, "understand": 0,
    "c3": 1, "application": 1, "apply": 1,
    "c4": 2, "analysis": 2, "analyze": 2,
    "c5": 2, "synthesis": 2, "evaluate": 2,
    "c6": 2, "evaluation": 2, "create": 2
}

class LocalOBEEngine:
    def __init__(self, artifacts_dir: str = None):
        if artifacts_dir is None:
            artifacts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
        self.artifacts_dir = artifacts_dir
        self.loaded = False
        self._load_artifacts()

    def _load_artifacts(self):
        # 1. Primary: Load embedded weights (zero filesystem IO, 100% cloud & Vercel compatible)
        try:
            from model.weights_data import WEIGHTS_DATA, VECTORIZER_META
            self.vocab = VECTORIZER_META["vocabulary"]
            self.idf = np.array(VECTORIZER_META["idf"], dtype=np.float32)
            self.input_dim = VECTORIZER_META["input_dim"]
            self.nn = FastNumPyInference(WEIGHTS_DATA)
            self.loaded = True
            return
        except Exception:
            pass

        # 2. Secondary: Fallback to reading files on disk
        weights_path = os.path.join(self.artifacts_dir, "model_weights.json")
        vectorizer_path = os.path.join(self.artifacts_dir, "vectorizer.json")

        if os.path.exists(weights_path) and os.path.exists(vectorizer_path):
            with open(weights_path, "r") as f:
                weights_data = json.load(f)
            with open(vectorizer_path, "r") as f:
                self.vec_meta = json.load(f)

            self.vocab = self.vec_meta["vocabulary"]
            self.idf = np.array(self.vec_meta["idf"], dtype=np.float32)
            self.input_dim = self.vec_meta["input_dim"]
            self.nn = FastNumPyInference(weights_data)
            self.loaded = True
            return

        raise FileNotFoundError(f"Model artifacts not found in {self.artifacts_dir}. Run `python -m model.train` first.")

    def _transform_text(self, text: str) -> np.ndarray:
        text_lower = text.lower()
        tokens = re.findall(r'(?u)\b\w+\b', text_lower)
        
        ngrams = list(tokens)
        for i in range(len(tokens) - 1):
            ngrams.append(f"{tokens[i]} {tokens[i+1]}")

        tf = np.zeros(len(self.idf), dtype=np.float32)
        for g in ngrams:
            if g in self.vocab:
                idx = self.vocab[g]
                tf[idx] += 1.0

        mask = tf > 0
        tf[mask] = 1.0 + np.log(tf[mask])

        tfidf = tf * self.idf
        norm = np.linalg.norm(tfidf)
        if norm > 0:
            tfidf = tfidf / norm

        verb_feat = np.zeros(3, dtype=np.float32)
        for v, tier in BLOOM_VERB_MAP.items():
            if re.search(r'\b' + re.escape(v) + r'\b', text_lower):
                verb_feat[tier] += 1.5

        if verb_feat.sum() > 0:
            verb_feat = verb_feat / verb_feat.sum()

        combined = np.concatenate([tfidf, verb_feat])
        return combined.astype(np.float32)

    def _extract_clo_level(self, clo_text: str) -> int:
        clo_lower = clo_text.lower()
        for code, tier in BLOOM_TIER_MAPPING.items():
            if re.search(r'\b' + re.escape(code) + r'\b', clo_lower):
                return tier
        for v, tier in BLOOM_VERB_MAP.items():
            if re.search(r'\b' + re.escape(v) + r'\b', clo_lower):
                return tier
        return 1

    def _generate_explanation(self, q_text: str, best_clo_text: str, cog_level: int) -> str:
        q_lower = q_text.lower()
        matched_verb = None
        for v in BLOOM_VERB_MAP.keys():
            if re.search(r'\b' + re.escape(v) + r'\b', q_lower):
                matched_verb = v
                break

        level_names = {0: "Level 1 knowledge", 1: "Level 2 application", 2: "Level 3 analysis/design"}
        level_str = level_names.get(cog_level, "cognitive level")

        if matched_verb:
            return f"Action verb '{matched_verb}' demands {level_str} fitting outcome"
        return f"Content semantics and complexity align with {level_str}"

    def match(self, questions: List[Dict[str, Any]], clos: List[str]) -> List[Dict[str, Any]]:
        if not clos:
            raise ValueError("Course learning outcomes (CLOs) list cannot be empty.")

        clo_tensors = np.vstack([self._transform_text(c) for c in clos])
        _, clo_embeddings = self.nn.forward(clo_tensors)
        clo_tiers = [self._extract_clo_level(c) for c in clos]

        results = []

        for q in questions:
            q_text = q.get("text", "")
            q_feat = self._transform_text(q_text)
            
            cog_probs, sem_emb = self.nn.forward(q_feat.reshape(1, -1))
            cog_probs = cog_probs[0]
            sem_emb = sem_emb[0]

            pred_cog_level = int(np.argmax(cog_probs))

            raw_scores = []
            for i in range(len(clos)):
                cos_sim = float(np.dot(sem_emb, clo_embeddings[i]))
                cos_sim_scaled = max(0.0, (cos_sim + 1.0) / 2.0)

                target_tier = clo_tiers[i]
                cog_fit = float(cog_probs[target_tier])

                q_words = set(re.findall(r'\b\w{4,}\b', q_text.lower()))
                clo_words = set(re.findall(r'\b\w{4,}\b', clos[i].lower()))
                overlap = len(q_words.intersection(clo_words))
                keyword_bonus = min(0.3, overlap * 0.08)

                score = (0.55 * cos_sim_scaled) + (0.35 * cog_fit) + keyword_bonus
                raw_scores.append(max(0.01, score))

            scores_arr = np.array(raw_scores, dtype=np.float32)
            temperature = 0.4
            exp_scores = np.exp(scores_arr / temperature)
            normalized_pct = (exp_scores / np.sum(exp_scores)) * 100.0

            rounded_scores = [int(round(s)) for s in normalized_pct]
            diff = 100 - sum(rounded_scores)
            best_idx = int(np.argmax(rounded_scores))
            rounded_scores[best_idx] += diff

            confidence = rounded_scores[best_idx]
            why_text = self._generate_explanation(q_text, clos[best_idx], pred_cog_level)

            declared_match = re.search(r'CLO[\s-]*(\d+)', q_text, re.IGNORECASE)
            declared_num = int(declared_match.group(1)) if declared_match else None
            is_discrepancy = False
            if declared_num is not None:
                if declared_num != (best_idx + 1):
                    is_discrepancy = True

            results.append({
                "scores": rounded_scores,
                "why": why_text,
                "best": best_idx,
                "conf": confidence,
                "cognitive_tier": pred_cog_level + 1,
                "declared_clo": declared_num,
                "discrepancy": is_discrepancy
            })

        return results

_engine = None

def get_engine() -> LocalOBEEngine:
    global _engine
    if _engine is None:
        _engine = LocalOBEEngine()
    return _engine
