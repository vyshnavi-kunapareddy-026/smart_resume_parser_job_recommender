import re
import os
import fitz  # PyMuPDF
import spacy
import joblib
from transformers import pipeline
from app.utils.layout_section_extractor import extract_sections_as_json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


ner_pipeline = pipeline(
    "token-classification",
    model="Jean-Baptiste/roberta-large-ner-english",
    aggregation_strategy="simple",
    framework="pt"
)
# --------- Text Extraction ----------
def extract_text_from_pdf(file_path):
    text = ""
    links = []

    with fitz.open(stream=file_path, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
            for link in page.get_links():
                if "uri" in link:
                    links.append(link["uri"])

    return text, links


# --------- Field Extraction ----------
def extract_email(text):
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match.group() if match else None


def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,}", text)
    return match.group() if match else None


def extract_links(text, extra_links=None):
    urls = re.findall(r'https?://[^\s]+', text)
    if extra_links:
        urls += extra_links
    urls = list(set(urls))

    linkedin, github, others = None, None, []
    for url in urls:
        if "linkedin.com" in url:
            linkedin = url
        elif "github.com" in url:
            github = url
        else:
            others.append(url)

    return {"linkedin": linkedin, "github": github, "websites": others}



'''
def extract_name_and_education_with_model(ner_pipeline, resume_json, label_fallback=True):
    header_text = resume_json.get("header", "")
    education_text = resume_json.get("education", "")

    entities_header = ner_pipeline(header_text)
    entities_edu = ner_pipeline(education_text)

    name_tokens = [e['word'] for e in entities_header if e["entity_group"] == "PER"]

    if not name_tokens and label_fallback:
        fallback_orgs = [
            e['word'] for e in entities_header
            if e["entity_group"] == "ORG"
            and e['word'].isupper()
            and 1 <= len(e['word'].split()) <= 3
        ]
        name_tokens = fallback_orgs

    name = " ".join(name_tokens).strip()
    org_tokens = [e['word'] for e in entities_edu if e["entity_group"] == "ORG"]
    education_orgs = list(set(org_tokens))

    return name, education_orgs'''

def extract_name_education_experience_with_model(
    ner_pipeline, resume_json, full_text="", label_fallback=True
):
    header_text = resume_json.get("header", "")
    education_text = resume_json.get("education", "")
    experience_text = resume_json.get("experience", "")

    # Run NER separately on each relevant part
    entities_header = ner_pipeline(header_text)
    entities_education = ner_pipeline(education_text) if education_text else []
    entities_experience = ner_pipeline(experience_text) if experience_text else []

    # ----- Name Extraction from header -----
    name_tokens = [e['word'] for e in entities_header if e["entity_group"].upper() == "PER"]
    if not name_tokens and label_fallback:
        fallback = [
            w for w in header_text.split('\n')[0].strip().split()
            if w.isalpha() and w.isupper()
        ]
        name_tokens = fallback
    name = " ".join(name_tokens).strip()

    # ----- Education Organizations from education section -----
    education_orgs = list({
        e['word'] for e in entities_education if e["entity_group"].upper() == "ORG"
    })

    # ----- Experience Organizations from experience section -----
    experience_orgs = list({
        e['word'] for e in entities_experience if e["entity_group"].upper() == "ORG"
    })

    return name, education_orgs, experience_orgs


def extract_skills(text, skills_list):
    text = text.lower()
    found = [skill for skill in skills_list if skill.lower() in text]
    return list(set(found))


# --------- Main Entry Point ----------
def parse_resume(filename, content, skills_list):
    extension = os.path.splitext(filename)[1].lower()
    if extension not in [".pdf", ".docx"]:
        return {"error": "Unsupported file format"}

    # Extract text & links
    text, extracted_links = extract_text_from_pdf(content)

    resume_json = extract_sections_as_json(content)


    # Extract layout-based sections (from PyMuPDF layout blocks)
    layout_sections = extract_sections_as_json(content)  # content is file-like (streamed bytes)



    # Extract structured fields
    email = extract_email(text)
    phone = extract_phone(text)
    links = extract_links(text, extracted_links)

    # NER-based name and education
    # name_general, edu_general = extract_name_and_education_with_model(ner_pipeline, resume_json)
    name_general, edu_general, experience_keywords = extract_name_education_experience_with_model(
    ner_pipeline, resume_json, text
    )

    # Rule-based skill matching
    skills = extract_skills(text, skills_list)
    print(f"Extracted skills in parser: {skills} type {type(skills)}")  # Debugging line

    return {
        "filename": filename,
        "name": name_general,
        "email": email,
        "phone": phone,
        "linkedin": links["linkedin"],
        "github": links["github"],
        "websites": links["websites"],
        "education": edu_general,
        "experience_keywords": experience_keywords,
        "skills": skills,
        "text_snippet": text[:500],         # For debug or preview
        "layout_sections": layout_sections  # New addition,

    }