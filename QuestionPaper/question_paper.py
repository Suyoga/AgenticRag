import fitz  
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract raw text from a question paper PDF
    
    :param pdf_path: location of the pdf
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text() + "\n"

    return full_text

def split_by_named_sections(text, SECTION_TITLES):
    """
    Segregates the text based on the question paper sections
    
    :param text: raw text after parsing pdf
    :param SECTION_TITLES: different sections of question paper
    """
    pattern = "(" + "|".join(map(re.escape, SECTION_TITLES)) + ")"
    parts = re.split(pattern, text)

    sections = {}
    for i in range(1, len(parts), 2):
        section_name = parts[i]
        section_text = parts[i + 1]
        sections[section_name] = section_text.strip()

    return sections


def extract_questions(text):
    """
    Splits text into questions
    
    :param text: raw text from pdf
    """
    pattern = r'(?m)^\s*(\d{1,2})\.\s+(.*?)(?=^\s*\d{1,2}\.\s+|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    questions = []
    for num, q in matches:
        q = q.strip()
        if len(q) < 10:   
            continue

        questions.append({
            "question_number": int(num),
            "question_text": q
        })

    return questions


