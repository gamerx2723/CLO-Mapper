"""
CLO Paper Checker - Application Launcher
Starts FastAPI server on http://localhost:8000
"""

import uvicorn
import os
import sys

def main():
    print("=" * 65)
    print("✦ CLO Paper Checker: Automated OBE Alignment Engine")
    print("✦ Mode: 100% Offline | Locally-Trained Neural Network | 0 API Keys")
    print("✦ Architecture: PyTorch Dual-Head Bloom Cognitive Classifier")
    print("✦ UI: Metallic & Glassmorphic Obsidian with Liquid Fluid Canvas")
    print("=" * 65)

    # Check if model artifacts exist; if not, train immediately
    artifacts_dir = os.path.join(os.path.dirname(__file__), "model", "artifacts")
    model_pt = os.path.join(artifacts_dir, "clo_model.pt")
    if not os.path.exists(model_pt):
        print("[*] Model weights not found. Training local neural model now...")
        from model.train import train
        train()

    print("[✓] Server starting at http://localhost:8000")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
