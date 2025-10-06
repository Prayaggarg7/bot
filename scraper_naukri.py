import requests
from bs4 import BeautifulSoup

def get_naukri_jobs(skills, location):
    jobs = []
    for skill in skills:
        url = f"https://www.naukri.com/{skill}-jobs-in-{location.lower()}"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.select("article.jobTuple.bgWhite.br4.mb-8")

        for card in cards:
            title_tag = card.find("a", class_="title")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = title_tag["href"]
            company = card.find("a", class_="subTitle")
            company = company.text.strip() if company else "N/A"
            date_tag = card.find("span", class_="job-post-day")
            date_posted = date_tag.text.strip() if date_tag else "N/A"
            jobs.append({
                "title": title,
                "company": company,
                "source": "Naukri",
                "link": link,
                "date_posted": date_posted
            })
    return jobs
