# 🧠 Smart Resume Parser & Recommender

A FastAPI-powered backend system that extracts structured information from resumes, generates summaries using an LLM, and provides a chatbot interface to ask questions about the uploaded resume.

---

## 🚀 Features

- 📄 Upload a resume (PDF)
- 🧠 Extract structured information:
  - Name, Email, Phone, LinkedIn, GitHub
  - Skills (matched from a predefined list)
  - Education Institutes
- 🔍 Layout-based section parsing (about, skills, experience, education) using PyMuPDF
- Named Entity Recognition using transformer models
- Job recommendations with match score
- 💬 Chatbot endpoint for querying resume content
- 🗃️ In-memory session support using `resume_id` (for later chat queries)
- FastAPI backend with modular code structure

---

## 📂 Project Structure

```
smart_resume_parser_job_recommender/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI app
│   │   ├── parser.py                    # Resume parsing logic
│   │   ├── recommender.py               # Job matching logic
│   │   ├── state.py                     # In-memory store for resume content
│   │   ├── utils/
│   │   │   ├── summarizer.py            # LLM-based summarization logic
│   │   │   ├── chatbot.py               # Q&A chatbot interface
│   │   │   └── layout_section_extractor.py  # Extracts structured resume sections
│   └── requirements.txt
├── resumes/                              # Folder to store uploaded resumes
├── notebooks/                            # Jupyter notebooks for experiments/trials
└── README.md

```

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/your-username/smart_resume_recommender.git
cd smart_resume_recommender/backend

# 2. Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI app
uvicorn app.main:app --reload
```

---

## 📬 API Endpoints

| Method | Endpoint         | Description                                  |
|--------|------------------|----------------------------------------------|
| POST   | `/upload-resume/`| Upload a PDF resume, extract and return info |
| POST   | `/chat`          | Ask a question based on uploaded resume      |

### Example: `/upload-resume/` Response

```json
{
  "resume_id": "<uuid>",
  "parsed": {
    "filename": "...",
    "name": "...",
    "email": "...",
    "linkedin": "...",
    "skills": [...],
    "education": [...],
    "text_snippet": "...",
    "layout_sections": {
      "header": "...",
      "about": "...",
      "skills": "...",
      "experience": "...",
      "education": "...",
      "additional_information": "..."
    },
    "recommended_jobs": [
      {
        "title": "...",
        "company": "...",
        "location": "...",
        "match_score": 50,
        "matched_skills": ["..."]
      }
    ]
  }
}
```

---

## 🔐 Model Info & Access

- Uses `transformers` from HuggingFace
- You’ll need a HuggingFace token with access to gated/public models
- Example model: `google/flan-t5-small` for summarization, `mistralai/Mistral-7B-Instruct-v0.2` if you switch to stronger LLMs

---

## 📌 TODO (Next Steps)

- 💼 Improve job recommendation logic in `recommender.py`
- 🗄️ Use PostgreSQL or SQLite to store uploaded resume metadata
- 🌐 Add frontend (optional)

---


---

## 📄 License

MIT License