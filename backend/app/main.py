from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from .parser import parse_resume
from .recommender import  recommend_jobs  # add this at the top
from fastapi import Body
from app.state import resume_store
from app.utils.chatbot import resume_chatbot
from fastapi import Query
from app.utils.adzuna_client import search_jobs_adzuna
import uuid
import json

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
    with open("skills.json", "r") as f:
        return json.load(f)



@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()

    skill_weights = load_skills()
    skills_list = list(skill_weights.keys())  # just the skill names for parsing

    parsed_data = parse_resume(file.filename, content, skills_list)

    resume_id = str(uuid.uuid4())
    resume_store[resume_id] = {
        "parsed": parsed_data,
        "weights": skill_weights  # optionally store weights with resume
    }

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

@app.get("/recommend-jobs/")
def recommend_jobs_endpoint(
    resume_id: str,
    role: str = Query(...),
    location: str = Query("India"),
    experience: str = Query("", description="Experience level like 'fresher', 'junior', 'senior'")
):
    resume_data = resume_store.get(resume_id)
    if not resume_data:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume_skills = resume_data.get("parsed", {}).get("skills", [])
    skill_weights = resume_data.get("weights", {})

    job_results = search_jobs_adzuna(role=role, location=location, experience=experience)

    recommendations = recommend_jobs(resume_skills, job_results)
    return {"recommendations": recommendations}


@app.get("/search-jobs/")
def search_jobs(
    role: str = Query(...),
    location: str = Query("India"),
    experience: str = Query("", description="Experience level like 'fresher', 'junior', 'senior'")
):
    jobs = search_jobs_adzuna(role=role, location=location, experience=experience)
    return {"results": jobs}