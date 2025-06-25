# 🧠 Smart Resume Parser + Job Recommender

This project is an end-to-end resume parsing and job recommendation system built using **FastAPI**. It extracts structured data from resumes (PDFs), summarizes key information, and recommends jobs in real time based on skills and experience.

## 🚀 Features

- 📄 **Resume Parsing**: Extracts name, contact info, education, experience, skills, and more from resumes using layout-aware PyMuPDF and NER models.
- 🔍 **Job Recommendation**: Fetches live jobs using the **Adzuna API** and ranks them based on skill/experience match.
- 🤖 **Named Entity Recognition**: Utilizes `Jean-Baptiste/roberta-large-ner-english` for name, education, and experience extraction.
- 🧠 **Skill Matching**: Matches resume skills with job descriptions using weighted scoring.
- 💬 **Resume Summary (LLM ready)**: Summarizes the parsed resume (future enhancement with LLMs).
- 🖥️ **Web Interface**: Upload resumes and view results visually in your browser.
- 🛠️ Built with **FastAPI**, **spaCy**, **transformers**, **PyMuPDF**, and more.

## 📁 Project Structure

```
smart_resume_parser_job_recommender/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── parser.py
│   │   ├── recommender.py
│   │   ├── utils/
│   │   │   ├── layout_section_extractor.py
│   │   └── templates/
│   │       ├── index.html
│   │       └── results.html
├── .env
├── requirements.txt
└── README.md
```

## ⚙️ How to Run Locally

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/smart_resume_parser_job_recommender.git
cd smart_resume_parser_job_recommender/backend
```

2. **Set up environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm
```

3. **Add your API key** in `.env` file:
```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

4. **Run the app**:
```bash
uvicorn app.main:app --reload
```

5. **Visit**: http://127.0.0.1:8000/upload


## 🛡️ Security Note

Make sure to **hide your `.env`** when pushing to GitHub. Add to `.gitignore`:

```
.env
*.ipynb
.ipynb_checkpoints/
```

## 🧪 Example Use Case

1. Upload your resume in PDF.
2. Parsed results and skills shown.
3. Get jobs matching your skills and experience.
4. Click "Details" to see job descriptions.

## 📦 Requirements

```
fastapi
uvicorn
python-multipart
PyMuPDF
spacy
scikit-learn
nltk
transformers
torch
joblib
requests
python-dotenv
```

Also include in `requirements.txt`:
```
en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
```

---

Made with ❤️ by Vyshnavi