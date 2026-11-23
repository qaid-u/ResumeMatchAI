"""Sample data and lightweight scoring used by demo mode.

Demo mode runs ResumeMatchAI with no MongoDB, Gemini key or ML models, so the UI
can be previewed anywhere. All people and companies below are fictional.
"""
import math
import re
from collections import Counter

JOBS = [
    {
        "position_name": "Data Scientist",
        "description": "Build and deploy machine learning models that rank and recommend content for a growing e-commerce platform.",
        "short_description": "Data Scientist with a degree in a quantitative field and 2+ years of ML experience. Works with Python, SQL and scikit-learn to build models, run experiments and present results to stakeholders.",
        "education": "- Bachelor's Degree in Computer Science, Statistics or Mathematics",
        "experience": "- 2+ years of experience building machine learning models",
        "responsibilities": "- Build and evaluate machine learning models\n- Design A/B experiments\n- Present findings to stakeholders",
        "technical_skills": "- Python\n- SQL\n- scikit-learn\n- Pandas\n- Machine Learning",
        "soft_skills": "- Communication\n- Problem-solving\n- Teamwork",
        "certifications": "- Google Professional Data Engineer (preferred)",
        "created_date": "02-11-2026",
    },
    {
        "position_name": "Frontend Developer",
        "description": "Create responsive, accessible web interfaces for a customer-facing analytics dashboard.",
        "short_description": "Frontend Developer with 3+ years of experience in React and TypeScript, focused on responsive, accessible interfaces, testing and close collaboration with designers.",
        "education": "- Diploma or Bachelor's Degree in Information Technology",
        "experience": "- 3+ years of frontend development experience",
        "responsibilities": "- Build reusable React components\n- Write unit tests\n- Work with designers on UI/UX",
        "technical_skills": "- JavaScript\n- TypeScript\n- React\n- HTML\n- CSS\n- Git",
        "soft_skills": "- Collaboration\n- Attention to detail",
        "certifications": "N/A",
        "created_date": "04-11-2026",
    },
    {
        "position_name": "Accountant",
        "description": "Maintain accounts payable and receivable, prepare monthly reports and support the annual audit.",
        "short_description": "Accountant with a degree in Accounting and 2+ years of experience in ledger management, reconciliations and financial reporting, comfortable with Excel and accounting software.",
        "education": "- Degree in Accounting",
        "experience": "- 2+ years of accounting experience",
        "responsibilities": "- Maintain general ledger\n- Prepare monthly financial reports\n- Support annual audit",
        "technical_skills": "- Microsoft Excel\n- SQL Accounting\n- Financial Reporting",
        "soft_skills": "- Integrity\n- Time management",
        "certifications": "- ACCA or CPA (preferred)",
        "created_date": "06-11-2026",
    },
]

CANDIDATES = [
    {
        "name": "Aisyah Rahman", "email_address": "aisyah.rahman@example.com", "phone_number": "+60123456701",
        "summary": "Data scientist with 4 years of experience building recommendation and forecasting models in Python.",
        "education": "- Master's Degree in Data Science\n- Bachelor's Degree in Statistics",
        "experience": "- 4 years of machine learning and data analysis experience",
        "technical_skills": "- Python\n- SQL\n- scikit-learn\n- Pandas\n- Machine Learning\n- TensorFlow",
        "soft_skills": "- Communication\n- Problem-solving\n- Teamwork",
        "certifications": "- Google Professional Data Engineer",
    },
    {
        "name": "Daniel Tan", "email_address": "daniel.tan@example.com", "phone_number": "+60123456702",
        "summary": "Frontend engineer with 5 years of experience shipping React and TypeScript applications.",
        "education": "- Bachelor's Degree in Information Technology",
        "experience": "- 5 years of frontend development experience",
        "technical_skills": "- JavaScript\n- TypeScript\n- React\n- HTML\n- CSS\n- Git\n- Jest",
        "soft_skills": "- Collaboration\n- Attention to detail",
        "certifications": "N/A",
    },
    {
        "name": "Nurul Huda", "email_address": "nurul.huda@example.com", "phone_number": "+60123456703",
        "summary": "Accountant with 3 years of experience in ledger management, reconciliations and audit support.",
        "education": "- Degree in Accounting",
        "experience": "- 3 years of accounting experience",
        "technical_skills": "- Microsoft Excel\n- SQL Accounting\n- Financial Reporting",
        "soft_skills": "- Integrity\n- Time management",
        "certifications": "- ACCA (Part qualified)",
    },
    {
        "name": "Farid Ismail", "email_address": "farid.ismail@example.com", "phone_number": "+60123456704",
        "summary": "Software engineer with full-stack experience, strong in Python and SQL, moving towards data roles.",
        "education": "- Bachelor's Degree in Computer Science",
        "experience": "- 2 years of software development experience",
        "technical_skills": "- Python\n- SQL\n- JavaScript\n- Git\n- Pandas",
        "soft_skills": "- Teamwork\n- Problem-solving",
        "certifications": "N/A",
    },
    {
        "name": "Mei Ling Chong", "email_address": "meiling.chong@example.com", "phone_number": "+60123456705",
        "summary": "Recent graduate in Information Technology with internship experience in web development.",
        "education": "- Diploma in Information Technology",
        "experience": "- 6 months internship in web development",
        "technical_skills": "- HTML\n- CSS\n- JavaScript\n- React",
        "soft_skills": "- Collaboration\n- Eagerness to learn",
        "certifications": "N/A",
    },
]

_STOP = {"the", "and", "of", "in", "a", "to", "for", "with", "or", "n", "years", "year", "degree", "experience"}


def _vec(text):
    words = re.findall(r"[a-z0-9+#]+", (text or "").lower())
    return Counter(w for w in words if w not in _STOP and len(w) > 1)


def match_score(resume_text, job_text):
    """Cosine similarity of bag-of-words vectors, scaled to 0-100 (a stand-in for BERT embeddings)."""
    a, b = _vec(resume_text), _vec(job_text)
    dot = sum(a[w] * b[w] for w in a)
    norm = math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values()))
    return round(dot / norm * 100, 2) if norm else 0.0


def match_comment(resume_text, job_text):
    a, b = _vec(resume_text), _vec(job_text)
    shared = sorted((w for w in a if w in b), key=lambda w: -b[w])[:6]
    if not shared:
        return "Demo comment: no overlapping skills or requirements were found between this resume and the job."
    return ("Demo comment (keyword overlap, no AI call): the resume shares these terms with the job requirements: "
            + ", ".join(shared) + ".")
