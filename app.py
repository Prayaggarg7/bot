from flask import Flask, render_template, request
import json
import os
from database import init_db, insert_jobs, get_all_jobs
from resume_parser import extract_skills_from_resume
from scraper_indeed import get_indeed_jobs
from scraper_naukri import get_naukri_jobs
from scraper_linkedin import get_linkedin_jobs

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

@app.route("/")
def index():
    jobs = get_all_jobs()
    query = request.args.get("q", "")
    if query:
        jobs = [job for job in jobs if query.lower() in job[0].lower() or query.lower() in job[1].lower()]
    return render_template("index.html", jobs=jobs, query=query)

@app.route("/fetch")
def fetch_jobs():
    if not os.path.exists("resume.pdf"):
        return "Resume file not found. Please add resume.pdf"
    init_db()
    skills = extract_skills_from_resume("resume.pdf")
    print("Extracted skills:", skills)
    indeed_jobs = get_indeed_jobs(skills, config["location"])
    naukri_jobs = get_naukri_jobs(skills, config["location"])
    linkedin_jobs = get_linkedin_jobs(skills, config["location"])

    all_jobs = indeed_jobs + naukri_jobs + linkedin_jobs
    insert_jobs(all_jobs)
    return f"✅ {len(all_jobs)} jobs fetched successfully."

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
