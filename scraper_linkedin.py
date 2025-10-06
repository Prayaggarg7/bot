import requests
from bs4 import BeautifulSoup

def get_linkedin_jobs(skills, location):
    jobs = []
    for skill in skills[:5]:  # limit to avoid blocking
        url = f"https://www.linkedin.com/jobs/search?keywords={skill}&location={location}"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        cards = soup.select("li[data-occludable-job-id]")
        for card in cards:
            title_tag = card.find("h3")
            company_tag = card.find("h4")
            link_tag = card.find("a")
            if not title_tag or not link_tag:
                continue
            title = title_tag.text.strip()
            company = company_tag.text.strip() if company_tag else "N/A"
            link = "https://www.linkedin.com" + link_tag["href"]
            jobs.append({
                "title": title,
                "company": company,
                "source": "LinkedIn",
                "link": link,
                "date_posted": "N/A"
            })
    return jobs
