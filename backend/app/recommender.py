import json
import os

def load_jobs(file_path="jobs.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def recommend_jobs(resume_skills, job_data, top_n=5):
    resume_skills_set = set([skill.lower() for skill in resume_skills])
    print("Resume Skills:", resume_skills_set)  # Debug

    recommendations = []

    for job in job_data:
        job_skills = set([skill.lower() for skill in job.get("required_skills", [])])
        matched_skills = resume_skills_set & job_skills
        # print(f"\nJob: {job['title']}")
        # print("Job Skills:", job_skills)
        # print("Matched:", matched_skills)

        if matched_skills:
            match_score = round((len(matched_skills) / len(job_skills)) * 100, 2)
            recommendations.append({
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location", "N/A"),
                "match_score": match_score,
                "matched_skills": list(matched_skills),
                "total_required_skills": len(job_skills),
                "total_matched_skills": len(matched_skills)
            })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_n]

