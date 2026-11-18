/**
 * CLO Paper Checker - Frontend Application Logic
 * Integrates with FastAPI Local Neural Inference Engine.
 */

(function () {
    let courses = [];
    let currentCourse = null;
    let currentClos = [];
    let currentQuestions = [];
    let currentMatchResult = null;

    // DOM Elements
    const courseSelect = document.getElementById("course-select");
    const closContainer = document.getElementById("clos-container");
    const cloCountBadge = document.getElementById("clo-count-badge");
    const btnAddClo = document.getElementById("btn-add-clo");
    const btnSampleExam = document.getElementById("btn-sample-exam");
    const examDropzone = document.getElementById("exam-dropzone");
    const fileInput = document.getElementById("file-input");
    const examText = document.getElementById("exam-text");
    const btnRunAlignment = document.getElementById("btn-run-alignment");
    const resultsSection = document.getElementById("results-section");
    const alignmentScoreVal = document.getElementById("alignment-score-val");
    const alignmentStatusBadge = document.getElementById("alignment-status-badge");
    const totalMarksLabel = document.getElementById("total-marks-label");
    const coverageBarsList = document.getElementById("coverage-bars-list");
    const alertsContainer = document.getElementById("alerts-container");
    const questionsTableBody = document.getElementById("questions-table-body");
    const parsedStats = document.getElementById("parsed-stats");
    const btnExportReport = document.getElementById("btn-export-report");
    const btnPrintReport = document.getElementById("btn-print-report");
    const btnImportCurriculum = document.getElementById("btn-import-curriculum");
    const curriculumFileInput = document.getElementById("curriculum-file-input");

    // Sample Exam Paper
    const SAMPLE_EXAM = `Question 1: [5 marks]
[CLO-1] Define encapsulation, data hiding, and abstract data types. Explain how access specifiers achieve encapsulation in C++.

Question 2: [10 marks]
Implement a complete Matrix class with dynamic memory allocation, copy constructor, and an overloaded + operator for matrix addition.

Question 3: [10 marks]
[CLO-1] Design an abstract Shape class hierarchy with pure virtual functions (area, perimeter) and implement Circle and Rectangle subclasses to demonstrate runtime polymorphism.

Question 4: [15 marks]
Critically evaluate the performance trade-offs between std::vector and std::list for arbitrary insertions and analyze cache locality implications.

Question 5: [10 marks]
Develop a custom exception hierarchy and write file serialization methods to store and restore Student objects to a binary file stream.`;

    // Initialize
    async function init() {
        try {
            const res = await fetch("/api/courses");
            courses = await res.json();
            renderCourseSelect();
            if (courses.length > 0) {
                selectCourse(courses[1]); // Default to CS2104 OOP
            }
        } catch (err) {
            console.error("Failed to fetch courses:", err);
            courseSelect.innerHTML = "<option>Failed to load courses</option>";
        }
    }

    function renderCourseSelect() {
        courseSelect.innerHTML = courses
            .map(c => `<option value="${c.code}">${c.code} - ${c.title}</option>`)
            .join("");

        courseSelect.addEventListener("change", (e) => {
            const found = courses.find(c => c.code === e.target.value);
            if (found) selectCourse(found);
        });
    }

    function selectCourse(course) {
        currentCourse = course;
        courseSelect.value = course.code;
        currentClos = [...course.clos];
        renderClos();
    }

    function renderClos() {
        cloCountBadge.textContent = `${currentClos.length} Outcomes`;
        closContainer.innerHTML = currentClos
            .map((clo, idx) => `
                <div class="clo-item">
                    <div>
                        <span class="tag">CLO-${idx + 1}</span>
                        <span>${escapeHtml(clo)}</span>
                    </div>
                    <button class="btn btn-secondary btn-sm" onclick="removeClo(${idx})" title="Remove CLO" style="padding: 2px 8px; font-size: 11px;">✕</button>
                </div>
            `).join("");
    }

    window.removeClo = function (index) {
        currentClos.splice(index, 1);
        renderClos();
    };

    btnAddClo.addEventListener("click", () => {
        const text = prompt("Enter CLO description (include Bloom tier, e.g., 'CLO-X (C3): Implement ...'):");
        if (text && text.trim()) {
            currentClos.push(text.trim());
            renderClos();
        }
    });

    btnSampleExam.addEventListener("click", () => {
        examText.value = SAMPLE_EXAM;
        parsedStats.textContent = "Sample exam loaded (5 questions, 50 marks)";
    });

    // File Drag & Drop
    examDropzone.addEventListener("click", () => fileInput.click());

    examDropzone.addEventListener("dragover", (e) => {
        e.preventDefault();
        examDropzone.classList.add("dragover");
    });

    examDropzone.addEventListener("dragleave", () => {
        examDropzone.classList.remove("dragover");
    });

    examDropzone.addEventListener("drop", async (e) => {
        e.preventDefault();
        examDropzone.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        const formData = new FormData();
        formData.append("file", file);

        examDropzone.querySelector(".dropzone-text").textContent = `Uploading & Parsing ${file.name}...`;

        try {
            const res = await fetch("/api/upload", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Upload failed");
            }

            const data = await res.json();
            examText.value = data.raw_text;
            parsedStats.textContent = `Parsed ${data.question_count} questions from ${data.filename}`;
            examDropzone.querySelector(".dropzone-text").textContent = `Loaded: ${file.name}`;
        } catch (err) {
            alert("Error parsing file: " + err.message);
            examDropzone.querySelector(".dropzone-text").textContent = "Drop Exam File (.pdf, .docx, .txt)";
        }
    }

    // Curriculum Importer
    btnImportCurriculum.addEventListener("click", () => curriculumFileInput.click());
    curriculumFileInput.addEventListener("change", async (e) => {
        if (e.target.files.length === 0) return;
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append("file", file);

        try {
            const res = await fetch("/api/parse-curriculum", { method: "POST", body: formData });
            const data = await res.json();
            if (data.courses && data.courses.length > 0) {
                courses = [...data.courses, ...courses];
                renderCourseSelect();
                selectCourse(data.courses[0]);
                alert(`Successfully imported ${data.courses_found} courses from ${file.name}!`);
            } else {
                alert("No course CLOs detected in curriculum file.");
            }
        } catch (err) {
            alert("Curriculum import failed: " + err.message);
        }
    });

    // Run Alignment
    btnRunAlignment.addEventListener("click", async () => {
        const text = examText.value.trim();
        if (!text) {
            alert("Please paste an exam paper or upload a file first.");
            return;
        }
        if (currentClos.length === 0) {
            alert("Please configure at least one CLO for the course.");
            return;
        }

        btnRunAlignment.disabled = true;
        btnRunAlignment.classList.add("loading-pulse");
        btnRunAlignment.textContent = "⚡ Running Local Neural Inference...";

        try {
            const questions = parseQuestionsFromText(text);
            currentQuestions = questions;

            const payload = {
                course_code: currentCourse ? currentCourse.code : "",
                course_title: currentCourse ? currentCourse.title : "",
                clos: currentClos,
                questions: questions
            };

            const res = await fetch("/api/match", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || "Alignment request failed");
            }

            currentMatchResult = await res.json();
            renderResults();
            resultsSection.style.display = "block";
            resultsSection.scrollIntoView({ behavior: "smooth" });
        } catch (err) {
            alert("Alignment failed: " + err.message);
        } finally {
            btnRunAlignment.disabled = false;
            btnRunAlignment.classList.remove("loading-pulse");
            btnRunAlignment.textContent = "⚡ Run Local Cognitive Alignment";
        }
    });

    function parseQuestionsFromText(rawText) {
        const lines = rawText.split("\n");
        const questions = [];
        let currentQ = null;

        const qRegex = /^\s*(?:(?:Question|Ques|Q)\s*[.\-#]?\s*)(\d{1,2}[a-zA-Z]?)\b[\s.:)\-]*(.*)$/i;
        const numRegex = /^\s*(\d{1,2}[a-zA-Z]?)\s*[.)]\s+(.*)$/;

        for (const line of lines) {
            const stripped = line.trim();
            if (!stripped) continue;

            const m = stripped.match(qRegex) || stripped.match(numRegex);
            if (m) {
                if (currentQ) {
                    currentQ.marks = extractMarks(currentQ.text);
                    questions.push(currentQ);
                }
                currentQ = { id: m[1], text: m[2] };
            } else {
                if (currentQ) {
                    currentQ.text += " " + stripped;
                }
            }
        }

        if (currentQ) {
            currentQ.marks = extractMarks(currentQ.text);
            questions.push(currentQ);
        }

        if (questions.length < 2) {
            const blocks = rawText.split(/\n\s*\n/).filter(b => b.trim().length > 20);
            if (blocks.length >= 2) {
                return blocks.map((b, idx) => ({
                    id: String(idx + 1),
                    text: b.trim(),
                    marks: extractMarks(b)
                }));
            }
        }

        return questions.length > 0 ? questions : [{ id: "1", text: rawText, marks: extractMarks(rawText) }];
    }

    function extractMarks(qText) {
        const bracketed = qText.match(/[\[(]\s*(\d+(?:\.\d+)?)\s*(?:marks?|pts?|points?)?\s*[\])]/i);
        if (bracketed) return parseFloat(bracketed[1]);
        const unbracketed = qText.match(/(\d+(?:\.\d+)?)\s*marks?/i);
        if (unbracketed) return parseFloat(unbracketed[1]);
        return 1.0;
    }

    function renderResults() {
        if (!currentMatchResult) return;

        const { alignment_pct, total_marks, total_questions, coverage, questions } = currentMatchResult;

        alignmentScoreVal.textContent = `${alignment_pct}%`;
        alignmentScoreVal.className = "gauge-score " + (alignment_pct >= 55 ? "score-pass" : alignment_pct >= 40 ? "score-warn" : "score-fail");

        if (alignment_pct >= 55) {
            alignmentStatusBadge.className = "badge badge-green mt-12";
            alignmentStatusBadge.textContent = "✓ OBE Accreditation Compliant";
        } else if (alignment_pct >= 40) {
            alignmentStatusBadge.className = "badge badge-lavender mt-12";
            alignmentStatusBadge.textContent = "⚠ Moderate Alignment (Review Needed)";
        } else {
            alignmentStatusBadge.className = "badge badge-red mt-12";
            alignmentStatusBadge.textContent = "✕ Deficient OBE Alignment (<40%)";
        }

        totalMarksLabel.textContent = `Total Marks: ${total_marks} | Total Questions: ${total_questions}`;

        coverageBarsList.innerHTML = coverage.map(cov => `
            <div class="coverage-row">
                <div class="coverage-info">
                    <span>
                        <strong>${cov.label}:</strong> ${escapeHtml(cov.text)}
                    </span>
                    <span style="font-family: var(--font-mono); color: ${cov.is_uncovered ? 'var(--red-400)' : 'var(--green-300)'};">
                        ${cov.marks} marks (${cov.percentage}%)
                    </span>
                </div>
                <div class="coverage-bar-track">
                    <div class="coverage-bar-fill ${cov.is_uncovered ? 'uncovered' : ''}" style="width: ${cov.is_uncovered ? 100 : Math.max(5, cov.percentage)}%;"></div>
                </div>
            </div>
        `).join("");

        const unassessed = coverage.filter(c => c.is_uncovered);
        const discrepancies = questions.filter(q => q.discrepancy);

        let alertsHtml = "";
        if (unassessed.length > 0) {
            alertsHtml += `
                <div class="discrepancy-banner" style="margin-bottom: 10px;">
                    <span style="font-size: 16px;">🚨</span>
                    <span><strong>OBE Deficiency Gap:</strong> ${unassessed.map(u => u.label).join(", ")} completely unassessed in this exam paper (0% coverage).</span>
                </div>
            `;
        }
        if (discrepancies.length > 0) {
            alertsHtml += `
                <div class="discrepancy-banner">
                    <span style="font-size: 16px;">⚠</span>
                    <span><strong>CLO Discrepancies Detected:</strong> ${discrepancies.length} question(s) have declared CLO markers that contradict cognitive complexity. Review questions below.</span>
                </div>
            `;
        }
        alertsContainer.innerHTML = alertsHtml;

        questionsTableBody.innerHTML = questions.map((q, idx) => {
            const tierBadge = q.cognitive_tier === 1
                ? '<span class="badge badge-lavender">Level 1 (Knowledge)</span>'
                : q.cognitive_tier === 2
                ? '<span class="badge badge-green">Level 2 (Application)</span>'
                : '<span class="badge badge-lavender" style="background: rgba(147, 51, 234, 0.25);">Level 3 (Analysis)</span>';

            const discrepancyHtml = q.discrepancy
                ? `<div class="discrepancy-banner">⚠ Paper says CLO-${q.declared_clo}, but neural model determined CLO-${q.best + 1}</div>`
                : "";

            return `
                <tr>
                    <td style="font-weight: 700; font-family: var(--font-mono); color: var(--lavender-300);">Q${q.id}</td>
                    <td class="question-text-cell">
                        ${escapeHtml(q.text)}
                        ${discrepancyHtml}
                    </td>
                    <td style="font-family: var(--font-mono); font-weight: 600;">${q.marks} pts</td>
                    <td>
                        <span class="badge badge-green">CLO-${q.best + 1}</span>
                    </td>
                    <td>${tierBadge}</td>
                    <td>
                        <div style="font-family: var(--font-mono); font-size: 12px; margin-bottom: 4px;">${q.conf}%</div>
                        <div class="coverage-bar-track" style="height: 4px; width: 60px;">
                            <div class="coverage-bar-fill" style="width: ${q.conf}%;"></div>
                        </div>
                    </td>
                    <td style="font-size: 12px; color: var(--text-secondary); max-width: 220px;">
                        ${escapeHtml(q.why)}
                    </td>
                    <td>
                        <select class="override-select" onchange="overrideQuestionClo(${idx}, this.value)">
                            ${currentClos.map((c, cIdx) => `
                                <option value="${cIdx}" ${cIdx === q.best ? 'selected' : ''}>CLO-${cIdx + 1}</option>
                            `).join("")}
                        </select>
                    </td>
                </tr>
            `;
        }).join("");
    }

    window.overrideQuestionClo = function (qIndex, newCloIndex) {
        newCloIndex = parseInt(newCloIndex, 10);
        if (!currentMatchResult || !currentMatchResult.questions[qIndex]) return;

        const q = currentMatchResult.questions[qIndex];
        q.best = newCloIndex;
        q.best_clo_label = `CLO-${newCloIndex + 1}`;
        q.conf = Math.max(75, q.conf);
        q.why = "Faculty manual override applied";
        q.discrepancy = false;

        recalculateObeStats();
        renderResults();
    };

    function recalculateObeStats() {
        const questions = currentMatchResult.questions;
        const numClos = currentClos.length;
        const totalMarks = questions.reduce((sum, q) => sum + q.marks, 0);

        const cloMarks = new Array(numClos).fill(0);
        const cloCounts = new Array(numClos).fill(0);
        let highConfCount = 0;

        for (const q of questions) {
            cloMarks[q.best] += q.marks;
            cloCounts[q.best] += 1;
            if (q.conf >= 50) highConfCount += 1;
        }

        currentMatchResult.alignment_pct = roundOneDecimal((highConfCount / questions.length) * 100);
        currentMatchResult.high_confidence_count = highConfCount;

        currentMatchResult.coverage = currentClos.map((cloText, idx) => ({
            clo_index: idx,
            label: `CLO-${idx + 1}`,
            text: cloText,
            marks: roundOneDecimal(cloMarks[idx]),
            count: cloCounts[idx],
            percentage: totalMarks > 0 ? roundOneDecimal((cloMarks[idx] / totalMarks) * 100) : 0,
            is_uncovered: cloCounts[idx] === 0
        }));
    }

    function roundOneDecimal(num) {
        return Math.round(num * 10) / 10;
    }

    function escapeHtml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    btnExportReport.addEventListener("click", () => {
        if (!currentMatchResult) return;
        const blob = new Blob([JSON.stringify(currentMatchResult, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `OBE_Alignment_Report_${currentCourse ? currentCourse.code : 'Exam'}.json`;
        a.click();
        URL.revokeObjectURL(url);
    });

    btnPrintReport.addEventListener("click", () => {
        window.print();
    });

    init();
})();