import fitz  
from pathlib import Path
from difflib import SequenceMatcher
import re


def extract_slide_pages(pdf_path):
    """
    Extracts one page at a time and cleans the text
    
    :param pdf_path: path of the course pdfs
    """
    doc = fitz.open(pdf_path)
    slides = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text = re.sub(r'\s*\d+\s*/\s*\d+\s*$', '', text).strip()
        slides.append({
            "page": page_num,
            "text": text
        })

    return slides

def extract_slide_title(slide_text):
    """
    Extracts title of a given slide
    
    :param slide_text: Content of the slide
    """
    lines = [l.strip() for l in slide_text.split("\n") if l.strip()]
    return lines[0] if lines else "Untitled"


def normalize_title(title):
    """
    Normalising slide title. Will be easier for comparison
    
    :param title: Slide title
    """
    title = title.lower()
    title = re.sub(r"(continued|\(cont\.\))", "", title)
    return title.strip()

def similar(a, b, threshold=0.85):
    """
    Returns true if the slide titles for 2 slides match with a 
    threshold greater than 0.85
    
    :param a: Title of Slide A
    :param b: Title of Slide B
    :param threshold: set Threshold
    """
    return SequenceMatcher(None, a, b).ratio() > threshold

def group_slides(slides):
    """
    Groups slides based on slide titles and their similarity
    
    :param slides: slides of all course content
    """
    groups = []
    current = None

    for slide in slides:
        title = extract_slide_title(slide["text"])
        norm_title = normalize_title(title)

        if (
            current
            and (
                norm_title == current["norm_title"]
                or similar(norm_title, current["norm_title"])
            )
        ):
            current["text"] += "\n" + slide["text"]
            current["page_range"][1] = slide["page"]
        else:
            if current:
                groups.append(current)

            current = {
                "title": title,
                "norm_title": norm_title,
                "text": slide["text"],
                "page_range": [slide["page"], slide["page"]],
            }

    if current:
        groups.append(current)

    return groups

def build_slide_chunks(pdf_path):
    """
    Chunking
    
    :param pdf_path: path of slides
    """
    slides = extract_slide_pages(pdf_path)
    groups = group_slides(slides)

    chunks = []
    for g in groups:
        chunks.append({
            "text": g["text"],
            "title": g["title"],
            "page_range": g["page_range"],
            "document": pdf_path
        })

    return chunks


def generate_chunks():

    pdf_folder = Path("../data")

    all_chunks = []

    for pdf_path in pdf_folder.glob("*.pdf"):
        if pdf_path.name == "exam_questions_optimization.pdf":
            continue
        
        chunks = build_slide_chunks(pdf_path)
        all_chunks.extend(chunks)

    return all_chunks
