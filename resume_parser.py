import os
from pdfminer.high_level import extract_text
import re

def extract_skills(resume_path="resume.pdf"):
    """
    Returns list of skills from resume.pdf or from SKILLS env variable.
    """
    env_skills = os.getenv("SKILLS")
    if env_skills:
        return [s.strip().lower() for s in env_skills.split(",") if s.strip()]

    if not os.path.exists(resume_path):
        return []

    text = extract_text(resume_path).lower()
    skill_list = [
        "python","java","spring boot","sql","mysql","mssql",
        "docker","kubernetes","aws","azure","node","linux",
        "git","rest api","hibernate","microservices","ci/cd"
    ]
    return [s for s in skill_list if re.search(r"\b" + re.escape(s) + r"\b", text)]
