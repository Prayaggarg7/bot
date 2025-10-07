from flask import Flask, render_template
from resume_parser import extract_skills
from job_scraper import scrape_indeed, scrape_naukri, scrape_linkedin
from telegram_notifier import send_telegram
from apscheduler.schedulers.background import BackgroundScheduler
import json, os, atexit

app = Flask(__name__)
JOBS_FILE = "jobs.json"
JOB_CACHE = []
LAST_FETCH_STATUS = "Never fetched"

# Load existing jobs
def load_jobs():
    global JOB_CACHE
    if os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, "r") as f:
            JOB_CACHE = json.load(f)

def save_jobs():
    with open(JOBS_FILE, "w") as f:
        json.dump(JOB_CACHE, f, indent=2)

def fetch_jobs():
    global JOB_CACHE, LAST_FETCH_STATUS
    skills = extract_skills()
    location = os.getenv("JOB_LOCATION", "India")
    jobs = []
    try:
        print("[INFO] Fetching jobs...")
        jobs += scrape_indeed(skills, location)
        jobs += scrape_naukri(skills, location)
        jobs += scrape_linkedin(skills, location)
        LAST_FETCH_STATUS = "Last fetch successful"
        print(f"[INFO] Fetched {len(jobs)} jobs")
    except Exception as e:
        LAST_FETCH_STATUS = f"Last fetch failed: {e}"
        print("[ERROR] Job fetch failed:", e)
        return

    # Deduplicate
    seen = set()
    new_jobs = []
    for j in jobs:
        key = (j["title"], j["company"], j["link"], j["source"])
        if key not in seen:
            seen.add(key)
            new_jobs.append(j)

    # Determine newly added jobs for Telegram
    to_notify = [j for j in new_jobs if j not in JOB_CACHE]

    JOB_CACHE = new_jobs
    save_jobs()

    # Send Telegram messages (if enabled)
    for job in to_notify:
        msg = f"💼 <b>{job['title']}</b>\n🏢 {job['company']}\n🌐 {job['source']}\n🔗 {job['link']}\n🗓️ {job['date_posted']}"
        send_telegram(msg)

# Load jobs on startup
load_jobs()

# Scheduler to fetch jobs every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_jobs, 'interval', minutes=15)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def index():
    jobs = sorted(JOB_CACHE, key=lambda x: x.get("date_posted",""), reverse=True)
    return render_template("index.html", jobs=jobs, status=LAST_FETCH_STATUS)

if __name__ == "__main__":
    print("[INFO] Starting Flask server...")
    fetch_jobs()  # initial fetch
    app.run(host="0.0.0.0", port=5000, debug=True)
