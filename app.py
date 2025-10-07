from flask import Flask, render_template, request, Response, redirect, url_for
from resume_parser import extract_skills
from job_scraper import scrape_indeed, scrape_naukri, scrape_linkedin, scrape_shine, scrape_timesjobs
from telegram_notifier import send_telegram
from apscheduler.schedulers.background import BackgroundScheduler
import json, os, atexit, time

app = Flask(__name__)
JOBS_FILE = "jobs.json"
JOB_CACHE = []
LAST_FETCH_STATUS = "Never fetched"

# ----------------- AUTH CONFIG -----------------
USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
PASSWORD = os.getenv("DASHBOARD_PASSWORD", "$%^Password@123")

def check_auth(u, p):
    return u == USERNAME and p == PASSWORD

def authenticate():
    return Response('Login required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.before_request
def require_auth():
    if not request.authorization or not check_auth(request.authorization.username, request.authorization.password):
        return authenticate()

# ----------------- JOB FUNCTIONS -----------------
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
        for scraper_name, scraper_func in [
            ("Indeed", scrape_indeed), 
            ("Naukri", scrape_naukri), 
            ("LinkedIn", scrape_linkedin),
            ("Shine", scrape_shine),
            ("TimesJobs", scrape_timesjobs)
        ]:
            try:
                result = scraper_func(skills, location)
                print(f"[INFO] {scraper_name}: fetched {len(result)} jobs")
                jobs += result
            except Exception as e:
                print(f"[ERROR] {scraper_name} scraper failed: {e}")
        LAST_FETCH_STATUS = "Last fetch successful"
        print(f"[INFO] Total jobs fetched: {len(jobs)}")
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

    # Filter last 15 days
    filtered_jobs = []
    for j in new_jobs:
        date_text = j.get("date_posted","")
        try:
            days = int(''.join(filter(str.isdigit, date_text))) if any(c.isdigit() for c in date_text) else 0
        except:
            days = 0
        if days <= 15:
            filtered_jobs.append(j)
    new_jobs = filtered_jobs

    # Determine newly added jobs for Telegram
    to_notify = [j for j in new_jobs if j not in JOB_CACHE]

    JOB_CACHE = new_jobs
    save_jobs()

    # Telegram notifications
    for job in to_notify:
        msg = f"💼 <b>{job['title']}</b>\n🏢 {job['company']}\n🌐 {job['source']}\n🔗 {job['link']}\n🗓️ {job['date_posted']}"
        try:
            send_telegram(msg)
        except Exception as e:
            print("[ERROR] Telegram send failed:", e)

# Load jobs on startup
load_jobs()

# Scheduler every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_jobs, 'interval', minutes=15)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# ----------------- FLASK ROUTES -----------------
@app.route("/")
def index():
    jobs = sorted(JOB_CACHE, key=lambda x: x.get("date_posted",""), reverse=True)
    return render_template("index.html", jobs=jobs, status=LAST_FETCH_STATUS)

@app.route("/refresh")
def refresh_jobs():
    fetch_jobs()
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("[INFO] Starting Flask server...")
    fetch_jobs()  # initial fetch
    app.run(host="0.0.0.0", port=5000, debug=True)
