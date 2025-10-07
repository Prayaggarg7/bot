import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# ------------------- INDEED -------------------
def scrape_indeed(skills, location):
    jobs = []
    query = "+".join(skills)
    url = f"https://www.indeed.co.in/jobs?q={query}&l={location}"
    try:
        print(f"[INFO][Indeed] Requesting URL: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        print(f"[INFO][Indeed] Status code: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR][Indeed] Failed to fetch jobs")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        for div in soup.find_all("div", {"class": "jobsearch-SerpJobCard"}):
            title_tag = div.find("h2", {"class": "title"})
            title = title_tag.text.strip() if title_tag else "N/A"
            company_tag = div.find("span", {"class": "company"})
            company = company_tag.text.strip() if company_tag else "N/A"
            link_tag = title_tag.find("a") if title_tag else None
            link = "https://www.indeed.co.in" + link_tag.get("href") if link_tag else "#"
            date_tag = div.find("span", {"class": "date"})
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            jobs.append({"title": title, "company": company, "link": link, "date_posted": date_posted, "source": "Indeed"})
        print(f"[INFO][Indeed] Parsed {len(jobs)} jobs")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR][Indeed] {e}")
    return jobs

# ------------------- NAUKRI -------------------
def scrape_naukri(skills, location):
    jobs = []
    query = "-".join(skills)
    url = f"https://www.naukri.com/{query}-jobs-in-{location}"
    try:
        print(f"[INFO][Naukri] Requesting URL: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        print(f"[INFO][Naukri] Status code: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR][Naukri] Failed to fetch jobs")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        for li in soup.find_all("li", {"class": "clearfix"}):
            title_tag = li.find("a", {"class": "title"})
            title = title_tag.text.strip() if title_tag else "N/A"
            company_tag = li.find("a", {"class": "subTitle"})
            company = company_tag.text.strip() if company_tag else "N/A"
            link = title_tag.get("href") if title_tag else "#"
            date_tag = li.find("span", {"class": "date"})
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            jobs.append({"title": title, "company": company, "link": link, "date_posted": date_posted, "source": "Naukri"})
        print(f"[INFO][Naukri] Parsed {len(jobs)} jobs")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR][Naukri] {e}")
    return jobs

# ------------------- LINKEDIN -------------------
def scrape_linkedin(skills, location):
    jobs = []
    query = "%20".join(skills)
    url = f"https://www.linkedin.com/jobs/search?keywords={query}&location={location}"
    try:
        print(f"[INFO][LinkedIn] Requesting URL: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        print(f"[INFO][LinkedIn] Status code: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR][LinkedIn] Failed to fetch jobs")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        for li in soup.find_all("li"):
            title_tag = li.find("h3")
            title = title_tag.text.strip() if title_tag else None
            company_tag = li.find("h4")
            company = company_tag.text.strip() if company_tag else None
            link_tag = li.find("a")
            link = "https://www.linkedin.com" + link_tag.get("href") if link_tag else None
            date_tag = li.find("time")
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            if title and company and link:
                jobs.append({"title": title, "company": company, "link": link, "date_posted": date_posted, "source": "LinkedIn"})
        print(f"[INFO][LinkedIn] Parsed {len(jobs)} jobs")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR][LinkedIn] {e}")
    return jobs

# ------------------- SHINE -------------------
def scrape_shine(skills, location):
    jobs = []
    query = "+".join(skills)
    url = f"https://www.shine.com/job-search/{query}-jobs-in-{location}"
    try:
        print(f"[INFO][Shine] Requesting URL: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        print(f"[INFO][Shine] Status code: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR][Shine] Failed to fetch jobs")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        for div in soup.find_all("div", {"class": "jobCard"}):
            title_tag = div.find("a", {"class": "jobTitle"})
            title = title_tag.text.strip() if title_tag else "N/A"
            company_tag = div.find("span", {"class": "compName"})
            company = company_tag.text.strip() if company_tag else "N/A"
            link = title_tag.get("href") if title_tag else "#"
            date_tag = div.find("span", {"class": "date"})
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            jobs.append({"title": title, "company": company, "link": link, "date_posted": date_posted, "source": "Shine"})
        print(f"[INFO][Shine] Parsed {len(jobs)} jobs")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR][Shine] {e}")
    return jobs

# ------------------- TIMESJOBS -------------------
def scrape_timesjobs(skills, location):
    jobs = []
    query = "-".join(skills)
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={query}&txtLocation={location}"
    try:
        print(f"[INFO][TimesJobs] Requesting URL: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        print(f"[INFO][TimesJobs] Status code: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR][TimesJobs] Failed to fetch jobs")
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        for li in soup.find_all("li", {"class": "clearfix job-bx"}):
            title_tag = li.find("h2")
            title = title_tag.text.strip() if title_tag else "N/A"
            company_tag = li.find("h3", {"class": "joblist-comp-name"})
            company = company_tag.text.strip() if company_tag else "N/A"
            link_tag = li.find("a")
            link = link_tag.get("href") if link_tag else "#"
            date_tag = li.find("span", {"class": "sim-posted"})
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            jobs.append({"title": title, "company": company, "link": link, "date_posted": date_posted, "source": "TimesJobs"})
        print(f"[INFO][TimesJobs] Parsed {len(jobs)} jobs")
        time.sleep(1)
    except Exception as e:
        print(f"[ERROR][TimesJobs] {e}")
    return jobs
