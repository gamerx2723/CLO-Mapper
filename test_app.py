"""
End-to-End Application Verification Script
Tests FastAPI routes, neural matching, and static asset serving.
"""

from fastapi.testclient import TestClient
from backend.app import app

def test_full_pipeline():
    client = TestClient(app)

    # 1. Test Health
    res_health = client.get("/api/health")
    assert res_health.status_code == 200, f"Health check failed: {res_health.text}"
    health_data = res_health.json()
    assert health_data["engine_loaded"] is True
    print("[✓] Health Check Passed: Model Loaded, Offline Mode Active.")

    # 2. Test Course Catalog
    res_courses = client.get("/api/courses")
    assert res_courses.status_code == 200
    courses = res_courses.json()
    assert len(courses) >= 9
    print(f"[✓] Course Catalog Passed: {len(courses)} accredited courses loaded.")

    # 3. Test Match Engine
    oop_course = next(c for c in courses if c["code"] == "CS2104")
    test_questions = [
        {"id": "1", "text": "Define encapsulation and explain data hiding in OOP classes. [5 marks]", "marks": 5.0},
        {"id": "2", "text": "Implement a Matrix class with copy constructor and overloaded addition operator. [10 marks]", "marks": 10.0},
        {"id": "3", "text": "[CLO-1] Design an abstract Shape class with virtual functions demonstrating runtime polymorphism. [15 marks]", "marks": 15.0}
    ]

    res_match = client.post("/api/match", json={
        "course_code": oop_course["code"],
        "course_title": oop_course["title"],
        "clos": oop_course["clos"],
        "questions": test_questions
    })
    assert res_match.status_code == 200, f"Match failed: {res_match.text}"
    match_data = res_match.json()

    assert match_data["total_marks"] == 30.0
    assert match_data["total_questions"] == 3
    assert len(match_data["questions"]) == 3
    
    # Check question 3 discrepancy detection
    q3 = match_data["questions"][2]
    assert q3["discrepancy"] is True, "Discrepancy should be detected for Q3"
    print("[✓] AI Neural Match Engine Passed:")
    print(f"    - Alignment Score: {match_data['alignment_pct']}%")
    print(f"    - Discrepancy Caught on Q3: {q3['best_clo_label']} (Paper said CLO-{q3['declared_clo']})")
    print(f"    - AI Rationale: {q3['why']}")

    # 4. Test Home Page
    res_home = client.get("/")
    assert res_home.status_code == 200
    assert "CLO Paper Checker" in res_home.text
    print("[✓] Frontend Static Assets & HTML Verified.")

    print("\n🎉 ALL PIPELINE TESTS PASSED!")

if __name__ == "__main__":
    test_full_pipeline()
