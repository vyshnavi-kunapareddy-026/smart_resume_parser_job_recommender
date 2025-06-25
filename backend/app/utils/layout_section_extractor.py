import fitz  # PyMuPDF
import re
from nltk.corpus import stopwords
from nltk import download
download('stopwords')

STOP_WORDS = set(stopwords.words("english"))

# Header standardization mapping
HEADER_GROUPS = {
    "about": ["about", "summary", "about me", "objective"],
    "education": ["education", "education details"],
    "skills": ["technical skills", "skills", "expertise", "strengths and expertise"],
    "experience": ["experience", "professional experience", "projects", "project experience"],
    "additional_information": ["additional information", "more about me", "certifications"]
}

def normalize_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

def match_standard_header(text):
    norm = normalize_text(text)
    for std_key, synonyms in HEADER_GROUPS.items():
        for variant in synonyms:
            if norm.startswith(variant):
                return std_key
    return None

def clean_text(text):
    words = re.findall(r'\b\w+\b', text)
    filtered = [w for w in words if w.lower() not in STOP_WORDS]
    return " ".join(filtered)

def extract_sections_as_json(file_bytes):
    # doc = fitz.open(pdf_path)
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    result = {}
    current_section = None

    for page in doc:
        blocks = page.get_text("blocks")
        blocks = [b for b in blocks if b[4].strip()]
        blocks.sort(key=lambda b: (b[1], b[0]))  # top to bottom, left to right

        for block in blocks:
            text = block[4].strip()
            section_key = match_standard_header(text)

            if section_key:
                current_section = section_key
                if section_key not in result:
                    result[section_key] = []
            elif current_section:
                result[current_section].append(text)

    # Final cleaning + merge section text
    for key in result:
        result[key] = " ".join(result[key]).strip()

    # Also extract topmost block as header
    first_page_blocks = doc[0].get_text("blocks")
    first_page_blocks = [b for b in first_page_blocks if b[4].strip()]
    topmost = min(first_page_blocks, key=lambda b: b[1])[4].strip()
    result["header"] = topmost

    return result

'''def extract_sections_as_json(file_bytes, spacing_threshold=20):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    # doc = fitz.open(pdf_path)
    page = doc[0]

    blocks = page.get_text("blocks")
    blocks = [b for b in blocks if b[4].strip()]
    blocks.sort(key=lambda b: b[1])  # top to bottom

    # Get topmost block for header
    topmost_block = min(blocks, key=lambda b: b[1])
    result = {"header": topmost_block[4].strip()}

    # Group into visual sections
    sections = []
    current_section = []
    prev_y1 = None

    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        if prev_y1 is not None and (y0 - prev_y1) > spacing_threshold:
            if current_section:
                sections.append(current_section)
                current_section = []
        current_section.append(block)
        prev_y1 = y1

    if current_section:
        sections.append(current_section)

    # Flatten and scan for headers
    all_blocks = [b for section in sections for b in section]
    all_blocks.sort(key=lambda b: b[1])

    current_key = None
    section_data = {}

    for block in all_blocks:
        raw_text = block[4].strip()
        std_key = match_standard_header(raw_text)
        if std_key:
            current_key = std_key
            if current_key not in section_data:
                section_data[current_key] = []
        elif current_key:
            section_data[current_key].append(raw_text)

    # Clean and assign to result
    for key, texts in section_data.items():
        full_text = " ".join(texts)
        cleaned = clean_text(full_text)
        result[key] = cleaned

    return result'''
