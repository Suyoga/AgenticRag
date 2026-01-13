import json
from pathlib import Path
from QuestionPaper.question_paper import extract_text_from_pdf, extract_questions, split_by_named_sections

final = {}

SECTION_META = {
    "Questions Requiring Small Proofs": 12,
    "Questions Requiring Extended Explanations": 10,
    "True/False and Multiple Choice": 12
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent

pdf_path = PROJECT_ROOT / "data" / "exam_questions_optimization.pdf"

text = extract_text_from_pdf(str(pdf_path))

sections = split_by_named_sections(text, list(SECTION_META.keys()))

for section, expected_count in SECTION_META.items():
        questions = extract_questions(sections.get(section, ""))

        final[section] = {
            "expected_count": expected_count,
            "actual_count": len(questions),
            "questions": questions
        }

with open("questions.json", "w") as f:
    json.dump(final, f)