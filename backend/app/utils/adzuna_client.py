import requests

ADZUNA_APP_ID = "0f21ed7e"
ADZUNA_APP_KEY = "4f343d93e7fb5264a666c8ea63ceaeba"
BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"  # 'in' for India

def search_jobs_adzuna(role: str, location: str = "India", results_limit: int = 20, experience: str = ""):
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_limit,
        "what": f"{experience} {role}" if experience else role,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        jobs = response.json().get("results", [])
        return [
            {
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "description": job.get("description"),
                "redirect_url": job.get("redirect_url"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max")
            }
            for job in jobs
        ]
    else:
        print(f"Adzuna API Error {response.status_code}: {response.text}")
        return []
