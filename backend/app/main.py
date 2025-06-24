from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from .parser import parse_resume
from .recommender import load_jobs, recommend_jobs  # add this at the top
from fastapi import Body
from app.state import resume_store
from app.utils.chatbot import resume_chatbot
import uuid

app = FastAPI()

# Optional: Allow frontend (Streamlit or React) to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Smart Resume Parser is live!"}

def load_skills():
    with open("skills.txt", "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

@app.get("/jobs/")
def get_jobs():
    jobs = load_jobs()
    return {"jobs": jobs}


@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    skills_list = load_skills()
    parsed_data = parse_resume(file.filename, content, skills_list)

    # Generate and store resume layout sections by ID (used for chatbot later)
    resume_id = str(uuid.uuid4())
    resume_store[resume_id] = parsed_data

    return {
        "resume_id": resume_id,
        "parsed": parsed_data
    }

@app.post("/chat")
def chat_with_resume(
    resume_id: str = Body(...),
    question: str = Body(...)
):
    layout = resume_store.get(resume_id)

    if not layout:
        return {"error": "Invalid resume ID or expired session"}

    answer = resume_chatbot(question, layout)
    return {"answer": answer}

@app.post("/recommend-jobs/")
def recommend_jobs_by_resume(resume_id: str):
    parsed_data = resume_store.get(resume_id)
    if not parsed_data:
        raise HTTPException(status_code=404, detail="Resume not found.")

    skills = parsed_data.get("skills", [])
    print(f"Extracted skills for recommendation: {skills}, type {type(skills)}")  # Debugging line
    job_data = load_jobs()  # from recommender.py
    recommendations = recommend_jobs(skills, job_data)
    return {"resume_id": resume_id, "recommended_jobs": recommendations}