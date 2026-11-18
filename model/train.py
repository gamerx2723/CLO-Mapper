"""
Local Training Script for OBE Cognitive Classifier & Semantic CLO Matcher
Runs 100% locally on GPU/CPU with 0 external API calls.
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import TfidfVectorizer

from model.dataset import TRAINING_DATA, BLOOM_VERB_MAP
from model.model_architecture import OBECognitiveNeuralNetwork

def build_training_tensors():
    texts = [item["question"] for item in TRAINING_DATA]
    cognitive_labels = [item["bloom_level"] for item in TRAINING_DATA]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=256,
        sublinear_tf=True,
        token_pattern=r'(?u)\b\w+\b'
    )
    X_tfidf = vectorizer.fit_transform(texts).toarray()

    verb_features = np.zeros((len(texts), 3), dtype=np.float32)
    for i, item in enumerate(TRAINING_DATA):
        q_lower = item["question"].lower()
        for verb, tier in BLOOM_VERB_MAP.items():
            if verb in q_lower:
                verb_features[i, tier] += 1.0
    
    row_sums = verb_features.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    verb_features = verb_features / row_sums

    X_combined = np.hstack([X_tfidf, verb_features]).astype(np.float32)
    vocab_dim = X_combined.shape[1]
    y_cognitive = np.array(cognitive_labels, dtype=np.int64)

    return X_combined, y_cognitive, vectorizer, vocab_dim

def train():
    print("=" * 60)
    print("🚀 Training Local OBE Cognitive Neural Model (Dual-Head)")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training device: {device}")

    X_train, y_cog, vectorizer, input_dim = build_training_tensors()
    print(f"[*] Dataset samples: {len(X_train)}, Input feature dim: {input_dim}")

    model = OBECognitiveNeuralNetwork(vocab_size=input_dim, embed_dim=128, hidden_dim=64, proj_dim=64).to(device)

    criterion_cog = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.015, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=120)

    X_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
    y_cog_tensor = torch.tensor(y_cog, dtype=torch.long).to(device)

    model.train()
    epochs = 120
    for epoch in range(1, epochs + 1):
        optimizer.zero_grad()
        cog_logits, sem_emb = model(X_tensor)

        loss_cog = criterion_cog(cog_logits, y_cog_tensor)
        gram = torch.matmul(sem_emb, sem_emb.T)
        eye = torch.eye(len(sem_emb), device=device)
        loss_contrastive = torch.mean((gram - eye) ** 2)

        total_loss = loss_cog + 0.3 * loss_contrastive
        total_loss.backward()
        optimizer.step()
        scheduler.step()

        if epoch % 20 == 0 or epoch == epochs:
            with torch.no_grad():
                preds = torch.argmax(cog_logits, dim=1)
                acc = (preds == y_cog_tensor).float().mean().item() * 100.0
            print(f"Epoch [{epoch:03d}/{epochs:03d}] - Loss: {total_loss.item():.4f} - Cognitive Acc: {acc:.1f}%")

    model.eval()
    with torch.no_grad():
        cog_logits, sem_emb = model(X_tensor)
        preds = torch.argmax(cog_logits, dim=1)
        final_acc = (preds == y_cog_tensor).float().mean().item() * 100.0

    print("=" * 60)
    print(f"✅ Training Complete! Final Cognitive Classification Accuracy: {final_acc:.2f}%")
    print("=" * 60)

    os.makedirs("model/artifacts", exist_ok=True)
    torch.save(model.state_dict(), "model/artifacts/clo_model.pt")
    print("[*] Saved PyTorch model: model/artifacts/clo_model.pt")

    clean_vocab = {k: int(v) for k, v in vectorizer.vocabulary_.items()}
    vectorizer_meta = {
        "vocabulary": clean_vocab,
        "idf": [float(x) for x in vectorizer.idf_.tolist()],
        "input_dim": int(input_dim)
    }
    with open("model/artifacts/vectorizer.json", "w") as f:
        json.dump(vectorizer_meta, f, indent=2)
    print("[*] Saved Vectorizer config: model/artifacts/vectorizer.json")

    numpy_export = model.export_numpy_weights()
    with open("model/artifacts/model_weights.json", "w") as f:
        json.dump(numpy_export, f)
    print("[*] Saved NumPy weights: model/artifacts/model_weights.json")

if __name__ == "__main__":
    train()
