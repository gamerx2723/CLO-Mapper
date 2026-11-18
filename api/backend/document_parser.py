"""
Document Parser and Question Extraction Engine
Supports PDF, DOCX, and Plain Text files with automatic question segmentation and marks weighting.
"""

import io
import re
from typing import List, Dict, Any, Tuple
import pypdf
import docx

def extract_text_from_file(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from PDF, DOCX, or TXT file bytes."""
    lower_name = filename.lower()
    
    if lower_name.endswith('.pdf'):
        pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text_parts = []
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_parts.append(extracted)
        return "\n\n".join(text_parts)

    elif lower_name.endswith('.docx') or lower_name.endswith('.doc'):
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        # Also parse table cells if present
        table_text = []
        for table in doc.tables:
            for row in table.rows:
                row_cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_cells:
                    table_text.append(" | ".join(row_cells))
        return "\n".join(paragraphs + table_text)

    else:
        # Default to UTF-8 decoding
        try:
            return file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return file_bytes.decode('latin-1', errors='replace')


def extract_marks(question_text: str) -> float:
    """
    Extract numerical marks/points allocation from question text.
    Matches bracketed marks: [5 marks], (10 pts), [2.5 points]
    and unbracketed: 10 marks, 5 marks
    """
    # 1. Bracketed regex
    bracketed = re.findall(r'[\[(]\s*(\d+(?:\.\d+)?)\s*(?:marks?|pts?|points?)?\s*[\])]', question_text, re.IGNORECASE)
    if bracketed:
        try:
            return float(bracketed[-1])
        except ValueError:
            pass

    # 2. Unbracketed regex
    unbracketed = re.findall(r'(\d+(?:\.\d+)?)\s*(?:marks?|pts?|points?)\b', question_text, re.IGNORECASE)
    if unbracketed:
        try:
            return float(unbracketed[-1])
        except ValueError:
            pass

    return 1.0  # Default unit weight if marks are unspecified


def split_questions(raw_text: str) -> List[Dict[str, Any]]:
    """
    Segments exam text into individual questions with question numbers, sub-parts, and marks.
    Follows splitQ heuristics from the specification.
    """
    lines = raw_text.splitlines()
    questions = []
    current_q = None

    q_pattern1 = re.compile(r'^\s*(?:(?:Question|Ques|Q)\s*[.\-#]?\s*)(\d{1,2}[a-zA-Z]?)\b[\s.:)\-]*(.*)$', re.IGNORECASE)
    q_pattern2 = re.compile(r'^\s*(\d{1,2}[a-zA-Z]?)\s*[.)]\s+(.*)$')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_q and current_q["text"]:
                current_q["text"] += "\n"
            continue

        m1 = q_pattern1.match(stripped)
        m2 = q_pattern2.match(stripped) if not m1 else None
        match = m1 or m2

        if match:
            # Save previous question
            if current_q and current_q["text"].strip():
                current_q["text"] = current_q["text"].strip()
                current_q["marks"] = extract_marks(current_q["text"])
                questions.append(current_q)

            q_id = match.group(1)
            rest = match.group(2)
            current_q = {
                "id": q_id,
                "text": rest.strip(),
                "marks": 1.0
            }
        else:
            if current_q is not None:
                current_q["text"] += " " + stripped
            else:
                # Header text before Question 1 or standalone text
                pass

    if current_q and current_q["text"].strip():
        current_q["text"] = current_q["text"].strip()
        current_q["marks"] = extract_marks(current_q["text"])
        questions.append(current_q)

    # Fallback heuristic: if fewer than 2 questions matched, split by double line breaks
    if len(questions) < 2:
        blocks = [b.strip() for b in re.split(r'\n\s*\n', raw_text) if len(b.strip()) > 20]
        if len(blocks) >= 2:
            questions = []
            for idx, block in enumerate(blocks, start=1):
                questions.append({
                    "id": str(idx),
                    "text": block,
                    "marks": extract_marks(block)
                })

    return questions


def parse_curriculum_text(text: str) -> List[Dict[str, Any]]:
    """
    Parse a curriculum / syllabus text containing multiple courses and CLOs.
    """
    lines = text.splitlines()
    courses = []
    current_course = None

    course_header_pattern = re.compile(r'(?:Course|Subject|Code)?\s*[:\-]?\s*([A-Z]{2,4}\s*[-]?\s*\d{3,4})\s*[:\-]?\s*(.*)', re.IGNORECASE)
    clo_pattern = re.compile(r'(?:CLO|Outcome)\s*[-_]?\s*(\d+)[:.\-]?\s*(.*)', re.IGNORECASE)

    for line in lines:
        s = line.strip()
        if not s:
            continue

        c_match = course_header_pattern.match(s)
        if c_match:
            if current_course and current_course["clos"]:
                courses.append(current_course)
            code = c_match.group(1).replace(" ", "").upper()
            title = c_match.group(2).strip() or "Course " + code
            current_course = {"code": code, "title": title, "clos": []}
            continue

        clo_match = clo_pattern.match(s)
        if clo_match and current_course:
            clo_num = clo_match.group(1)
            clo_desc = clo_match.group(2).strip()
            current_course["clos"].append(f"CLO-{clo_num}: {clo_desc}")
        elif current_course and len(current_course["clos"]) > 0 and len(s) > 10:
            # Append multiline CLO description
            current_course["clos"][-1] += " " + s

    if current_course and current_course["clos"]:
        courses.append(current_course)

    return courses
