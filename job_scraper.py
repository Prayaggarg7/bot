import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time, re

def log_error(source, e):
    print(f"[ERROR] {source} scraper failed: {e}")

def parse_days_ago(text):
    t = (text or "").lower()
    if "just" in t or "today" in t:
        return 0
    m = re.search(r"(\d+)\s+day", t)
    if m:
        return int(m.group(1))
    m2 = re.search(r"(\d+)\s+hour", t)
    if m2:
        return 0
    return None

# ----------------- Indeed -----------------
def scrape_indeed(skills, location="India", pages=2, days_back=15):
    jobs = []
    ua = {"User-Agent": "Mozilla/5.0"}
    for skill in skills[:5]:
        for p in range(pages):
            start = p * 10
            url = f"https://www.indeed.com/jobs?q={quote_plus(skill)}&l={quote_plus(location)}&start={start}"
            try:
                r = requests.get(url, headers=ua, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "lxml")
                cards = soup.select("div.job_seen_beacon")
                for c in cards:
                    title = (c.find("h2") or c.find("h3")).get_text(strip=True) if (c.find("h2") or c.find("h3")) else ""
                    company = (c.find("span", {"class":"companyName"}) or c.find("span", {"class":"company"}))
                    company = company.get_text(strip=True) if company else ""
                    link_tag = c.find("a", href=True)
                    link = "https://www.indeed.com" + link_tag["href"] if link_tag and not link_tag["href"].startswith("http") else (link_tag["href"] if link_tag else "")
                    date_tag = c.find("span", string=lambda s: s and ("day" in s.lower() or "hour" in s.lower() or "today" in s.lower()))
                    date_posted = date_tag.get_text(strip=True) if date_tag else ""
                    days = parse_days_ago(date_posted)
                    if days is not None and days > days_back:
                        continue
                    jobs.append({"title": title, "company": company, "link": link, "source": "Indeed", "date_posted": date_posted})
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                log_error("Indeed", e)
    return jobs

# ----------------- Naukri -----------------
def scrape_naukri(skills, location="India", pages=2, days_back=15):
    jobs = []
    ua = {"User-Agent": "Mozilla/5.0"}
    for skill in skills[:4]:
        for p in range(1, pages+1):
            url = f"https://www.naukri.com/{quote_plus(skill)}-jobs-in-{quote_plus(location)}?k={quote_plus(skill)}&pageno={p}"
            try:
                r = requests.get(url, headers=ua, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "lxml")
                cards = soup.select("article.jobTuple")
                for c in cards:
                    title_tag = c.select_one("a.title")
                    title = title_tag.get_text(strip=True) if title_tag else ""
                    link = title_tag["href"] if title_tag and title_tag.has_attr("href") else ""
                    company_tag = c.select_one("a.subTitle")
                    company = company_tag.get_text(strip=True) if company_tag else ""
                    date_tag = c.select_one("div.type") or c.select_one("span.postedOn")
                    date_posted = date_tag.get_text(strip=True) if date_tag else ""
                    days = parse_days_ago(date_posted)
                    if days is not None and days > days_back:
                        continue
                    jobs.append({"title": title, "company": company, "link": link, "source": "Naukri", "date_posted": date_posted})
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                log_error("Naukri", e)
    return jobs

# ----------------- LinkedIn -----------------
def scrape_linkedin(skills, location="India", pages=2, days_back=15):
    jobs = []
    ua = {"User-Agent": "Mozilla/5.0"}
    for skill in skills[:3]:
        for p in range(pages):
            offset = p * 25
            url = f"https://www.linkedin.com/jobs/search?keywords={quote_plus(skill)}&location={quote_plus(location)}&start={offset}"
            try:
                r = requests.get(url, headers=ua, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "lxml")
                cards = soup.select("ul.jobs-search__results-list li")
                for c in cards:
                    title_tag = c.select_one("h3")
                    title = title_tag.get_text(strip=True) if title_tag else ""
                    company_tag = c.select_one("h4")
                    company = company_tag.get_text(strip=True) if company_tag else ""
                    date_tag = c.select_one("time")
                    date_posted = date_tag.get_text(strip=True) if date_tag else ""
                    days = parse_days_ago(date_posted)
                    if days is not None and days > days_back:
                        continue
                    link_tag = c.select_one("a")
                    link = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""
                    jobs.append({"title": title, "company": company, "link": link, "source": "LinkedIn", "date_posted": date_posted})
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                log_error("LinkedIn", e)
    return jobs
