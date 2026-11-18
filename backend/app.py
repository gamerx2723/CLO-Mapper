"""
FastAPI Server for CLO Paper Checker & OBE Analysis
Runs with locally trained PyTorch neural model - 0 API keys required.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from model.inference import get_engine
from backend.catalog import COURSE_CATALOG
from backend.document_parser import extract_text_from_file, split_questions, parse_curriculum_text

app = FastAPI(
    title="CLO Paper Checker & OBE Alignment",
    description="Automated OBE Exam Paper Alignment with locally-trained neural Bloom's taxonomy classifier.",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request / Response Schemas
class QuestionItem(BaseModel):
    id: Optional[str] = "1"
    text: str
    marks: Optional[float] = 1.0

class MatchRequest(BaseModel):
    course_code: Optional[str] = ""
    course_title: Optional[str] = ""
    clos: List[str]
    questions: List[QuestionItem]

class RetrainRequest(BaseModel):
    epochs: Optional[int] = 100

@app.get("/api/health")
def health_check():
    engine = get_engine()
    return {
        "status": "healthy",
        "engine_loaded": engine.loaded,
        "mode": "offline-local-neural",
        "device": "Local CPU/RTX 5050 GPU",
        "api_keys_required": False
    }

@app.get("/api/courses")
def get_courses():
    return COURSE_CATALOG

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload exam paper (.pdf, .docx, .txt) and extract segmented questions with marks."""
    allowed_exts = (".pdf", ".docx", ".doc", ".txt")
    if not any(file.filename.lower().endswith(ext) for ext in allowed_exts):
        raise HTTPException(status_code=400, detail="Invalid file type. Supported formats: .pdf, .docx, .txt")

    content = await file.read()
    raw_text = extract_text_from_file(content, file.filename)
    questions = split_questions(raw_text)

    return {
        "filename": file.filename,
        "raw_text": raw_text,
        "question_count": len(questions),
        "questions": questions
    }

@app.post("/api/match")
def match_questions(req: MatchRequest):
    """
    Match questions against Course Learning Outcomes (CLOs) using the local neural model.
    Calculates:
    - Overall alignment percentage
    - Marks-weighted CLO coverage distribution
    - Discrepancy flags (paper says CLO-X vs predicted CLO-Y)
    - Bloom's cognitive tiers (Level 1, 2, 3)
    """
    if not req.clos:
        raise HTTPException(status_code=400, detail="Course learning outcomes (CLOs) cannot be empty.")
    if not req.questions:
        raise HTTPException(status_code=400, detail="No questions provided for alignment.")

    engine = get_engine()
    q_dicts = [{"text": q.text, "marks": q.marks or 1.0} for q in req.questions]
    match_results = engine.match(q_dicts, req.clos)

    # Calculate OBE Paper Metrics
    num_questions = len(req.questions)
    num_clos = len(req.clos)
    total_paper_marks = sum(q.marks or 1.0 for q in req.questions)

    # Marks-weighted distribution per CLO
    clo_weighted_marks = [0.0] * num_clos
    clo_question_counts = [0] * num_clos
    high_conf_count = 0

    enriched_questions = []
    for idx, (q, res) in enumerate(zip(req.questions, match_results)):
        weight = q.marks if (q.marks and q.marks > 0) else 1.0
        best_clo = res["best"]
        conf = res["conf"]

        clo_weighted_marks[best_clo] += weight
        clo_question_counts[best_clo] += 1

        if conf >= 50:
            high_conf_count += 1

        enriched_questions.append({
            "id": q.id or str(idx + 1),
            "text": q.text,
            "marks": weight,
            "best": best_clo,
            "best_clo_label": f"CLO-{best_clo + 1}",
            "conf": conf,
            "cognitive_tier": res["cognitive_tier"],
            "scores": res["scores"],
            "why": res["why"],
            "declared_clo": res.get("declared_clo"),
            "discrepancy": res.get("discrepancy", False)
        })

    # Overall Paper Alignment Score
    alignment_pct = round((high_conf_count / num_questions) * 100.0, 1) if num_questions > 0 else 0.0

    # CLO Distribution Percentages
    clo_coverage = []
    for i in range(num_clos):
        pct = round((clo_weighted_marks[i] / total_paper_marks) * 100.0, 1) if total_paper_marks > 0 else 0.0
        clo_coverage.append({
            "clo_index": i,
            "label": f"CLO-{i + 1}",
            "text": req.clos[i],
            "marks": round(clo_weighted_marks[i], 1),
            "count": clo_question_counts[i],
            "percentage": pct,
            "is_uncovered": (clo_question_counts[i] == 0)
        })

    return {
        "alignment_pct": alignment_pct,
        "total_marks": total_paper_marks,
        "total_questions": num_questions,
        "high_confidence_count": high_conf_count,
        "coverage": clo_coverage,
        "questions": enriched_questions
    }

@app.post("/api/parse-curriculum")
async def parse_curriculum(file: UploadFile = File(...)):
    """Parse entire curriculum PDF or text document into course CLO sets."""
    content = await file.read()
    raw_text = extract_text_from_file(content, file.filename)
    parsed_courses = parse_curriculum_text(raw_text)
    return {
        "filename": file.filename,
        "courses_found": len(parsed_courses),
        "courses": parsed_courses
    }

# Mount static files and SPA root
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_home():
    root_index = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
    if os.path.exists(root_index):
        return FileResponse(root_index)
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "CLO Mapper API is active. Static frontend index.html not found."}
