import requests
from bs4 import BeautifulSoup

def get_indeed_jobs(skills, location):
    jobs = []
    for skill in skills:
        for start in range(0, 50, 10):  # up to 5 pages
            url = f"https://www.indeed.com/jobs?q={skill}&l={location}&start={start}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            cards = soup.select("div.job_seen_beacon")

            if not cards:
                break

            for card in cards:
                title_tag = card.find("h2")
                if not title_tag:
                    continue
                title = title_tag.text.strip()
                company = card.find("span", {"class": "companyName"})
                company = company.text.strip() if company else "N/A"
                date_span = card.find("span", string=lambda x: x and ("day" in x or "Just" in x))
                date_posted = date_span.text.strip() if date_span else "N/A"
                link = card.find("a")["href"]
                job_link = f"https://www.indeed.com{link}"
                jobs.append({
                    "title": title,
                    "company": company,
                    "source": "Indeed",
                    "link": job_link,
                    "date_posted": date_posted
                })
    return jobs
