import re
from pdfminer.high_level import extract_text

def extract_skills_from_resume(resume_path):
    text = extract_text(resume_path).lower()

    # Basic keyword list – you can expand this anytime
    skill_list = [
        "python", "java", "angular", "spring boot", "sql", "mysql", "mssql",
        "docker", "kubernetes", "aws", "azure", "react", "typescript", "html",
        "css", "javascript", "node", "git", "linux", "automation"
    ]

    found = [skill for skill in skill_list if re.search(r'\b' + re.escape(skill) + r'\b', text)]
    return list(set(found))
