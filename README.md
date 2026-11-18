# CLO Paper Checker: Automated OBE Exam Paper Alignment & Analysis

> **100% Offline AI Tool** for Outcome-Based Education (OBE) accreditation. Parses exam papers, extracts questions and marks, and maps them to Course Learning Outcomes (CLOs) using a **locally-trained PyTorch Dual-Head Neural Network** based on Bloom's Taxonomy cognitive levels—**with Zero API Keys**.

---

## Visual Design & Experience
- **Interactive Liquid Fluid Canvas**: Real-time fluid dynamic ripples and viscous waves that interact with cursor movements and velocities.
- **Metallic & Glassmorphism Aesthetic**: Deep obsidian black glass surfaces (`#07070a`), brushed titanium and specular borders, frosted card backdrops (`backdrop-filter: blur(20px)`).
- **Lavender-Green & Crimson Red Accents**:
  - **Lavender (`#c084fc`)**: AI cognitive reasoning, Bloom taxonomy indicators, and neural status pills.
  - **Emerald Green (`#10b981`)**: OBE accreditation compliance passes, high-confidence match bars, and verified metrics.
  - **Crimson Red (`#ef4444`)**: Unassessed outcome gaps (`Not covered`) and declared discrepancy alerts (`⚠ paper says CLO-X`).

---

## Key Capabilities & Features

| Capability | Description |
| :--- | :--- |
| **Zero API Keys & 100% Offline** | Powered by an in-house trained PyTorch dual-head neural model (`OBECognitiveNeuralClassifier`) running locally on CPU/GPU. No external API calls or subscription costs. |
| **Instant Inference Latency** | Sub-millisecond (<5ms per question) neural forward pass with pure NumPy fallback runtime. |
| **Multi-Format Ingestion** | Ingests `.pdf` (via `pypdf`), `.docx` Word documents (via `python-docx`), and plain text with automatic line-preserving heuristics. |
| **Intelligent Question Segmentation** | Detects question numbers, sub-parts, and multiline question text (`splitQ` algorithm). |
| **Automated Marks Weighting** | Extracts point allocations (e.g., `[5 marks]`, `(10 pts)`) to calculate marks-weighted exam coverage rather than simple question counts. |
| **Cognitive Tier Matching** | Classifies questions into Level 1 (Remember/Understand), Level 2 (Apply/Solve), and Level 3 (Analyze/Design/Evaluate). |
| **Discrepancy Auditing** | Flags discrepancies when an instructor labels "CLO-1" on the paper but the question demands "CLO-3" application or design complexity. |
| **OBE Deficiency Gap Alerts** | Prominently highlights any unassessed CLO (0% coverage) before exams are administered. |
| **Human-in-the-Loop Overrides** | Faculty can manually adjust any question's assigned CLO via an interactive dropdown; all paper-wide metrics dynamically recalculate. |
| **Preloaded 9-Course Catalog** | Comes preconfigured with accredited computing courses (Programming, OOP, DSA, OS, Software Architecture, AI, SQE, SPM, Automata). |
| **Bulk Curriculum Importer** | Ingests an entire university curriculum/syllabus PDF and extracts course CLO sets automatically. |

---

## Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/gamerx2723/CLO-Mapper.git
cd CLO-Mapper
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python run.py
```
Open your browser at:
```
http://localhost:8000
```
