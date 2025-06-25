import json
import os
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load weighted skills dictionary
def load_weighted_skills(file_path="skills.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def recommend_jobs(resume_skills, job_data, top_n=10):
    skill_weights = load_weighted_skills()
    resume_skills_set = set(skill.lower() for skill in resume_skills)
    resume_text = ", ".join(resume_skills_set)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    recommendations = []

    for job in job_data:
        job_description = job.get("description", "")
        job_embedding = model.encode(job_description, convert_to_tensor=True)

        # Semantic similarity
        semantic_score = util.pytorch_cos_sim(resume_embedding, job_embedding).item()
        semantic_score_pct = round(semantic_score * 100, 2)

        # Weighted skill match
        job_skills = set()
        job_description_lower = job_description.lower()
        weighted_score = 0
        total_weight = 0

        for skill in resume_skills_set:
            if skill in job_description_lower:
                weight = skill_weights.get(skill, 0.5)  # default weight = 0.5 if not listed
                weighted_score += weight
            total_weight += skill_weights.get(skill, 0.5)

        weighted_match_pct = round((weighted_score / total_weight) * 100, 2) if total_weight else 0

        # Hybrid score
        final_score = round((0.7 * semantic_score_pct) + (0.3 * weighted_match_pct), 2)

        # Formatting
        matched_skills = [skill for skill in resume_skills_set if skill in job_description_lower]
        missing_skills = [skill for skill in job_description_lower.split() if skill in skill_weights and skill not in resume_skills_set]

        company = job.get("company")
        if isinstance(company, str):
            company_name = company
        elif isinstance(company, dict):
            company_name = company.get("display_name", "Unknown")
        else:
            company_name = "Unknown"

        location = job.get("location")
        if isinstance(location, str):
            location_name = location
        elif isinstance(location, dict):
            location_name = location.get("display_name", "N/A")
        else:
            location_name = "N/A"

        recommendations.append({
            "title": job.get("title"),
            "company": company_name,
            "location": location_name,
            "job_url": job.get("redirect_url"),
            "salary_min": job.get("salary_min"),
            "description": job_description,
            "semantic_relevance": semantic_score_pct,
            "weighted_skill_match": weighted_match_pct,
            "match_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_n]
