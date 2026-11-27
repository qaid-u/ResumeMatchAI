<div align="center">

# ResumeMatchAI

**Match resumes to job descriptions, score every candidate and get a ranked shortlist with AI comments.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?logo=spacy&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=googlegemini&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?logo=mongodb&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

---

## 🎬 Demo

The screenshots below come from **demo mode**: fictional jobs and candidates, no database and no API key required. Run it yourself in two commands (see [Try it](#try-it-with-no-setup-demo-mode)).

<p align="center">
  <img src="docs/screenshots/jobs.png" alt="Job descriptions list with Detail, Update and Delete actions" width="100%"><br>
  <sub><b>Jobs</b>: browse job descriptions (Data Scientist, Frontend Developer, Accountant in the sample data) with Detail / Update / Delete actions.</sub>
</p>

<p align="center">
  <img src="docs/screenshots/matching-results.png" alt="Matched candidates sorted by score" width="100%"><br>
  <sub><b>Matching</b>: pick a job and click Match Candidates to get candidates sorted by match score, with contact details and a comment per candidate.</sub>
</p>

## Features

- **AI matching**: scores candidates against a job description (cosine similarity of sentence embeddings in full mode; keyword overlap in demo mode).
- **Candidate ranking**: automatically sorts candidates by match score for easy comparison.
- **Detailed feedback**: a summary and comment for each candidate based on their match; the Gemini API extracts name, email, phone, summary, education, experience, technical and soft skills and certifications from resumes.
- **Streamlit UI** with Jobs, Candidates and Matching pages.
- **MongoDB integration**: stores candidate resumes, job descriptions and matching results.
- **Demo mode**: in-memory sample data, no external services.

## Tech stack

| Area | Technology |
| --- | --- |
| UI | Streamlit |
| Language | Python |
| NLP | spaCy, sentence-transformers (embeddings), Gemini API (Google Generative AI) |
| Documents / OCR | PyPDF2, python-docx, pytesseract, pdf2image |
| Database | MongoDB (pymongo); mongomock in demo mode |

## Try it with no setup (demo mode)

The app runs in **demo mode** whenever `MONGODB_URI` is not set (or `DEMO_MODE=1`). It uses an in-memory database seeded with fictional jobs and candidates (`demo_data.py`) and scores matches by keyword overlap instead of calling Gemini, so no database, API key or ML models are needed.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Uploading jobs and resumes is disabled in demo mode, since it needs Gemini and OCR.

<details>
<summary><b>Host the demo for free (Streamlit Community Cloud)</b></summary>

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app**, pick this repo, branch `main`, main file `app.py`.
3. Deploy without setting any secrets, so it starts in demo mode.
4. Add the resulting URL here as a "Live demo" link.

</details>

## Full installation

<details>
<summary><b>Prerequisites and steps</b></summary>

Prerequisites:

- Python 3.8+
- Tesseract OCR (for scanned PDFs) and the spaCy model: `python -m spacy download en_core_web_sm`
- A MongoDB database (cloud or local)
- An API key for the Gemini API

Steps:

```bash
git clone https://github.com/qaid-u/ResumeMatchAI.git
cd ResumeMatchAI
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements-full.txt
```

Create a `.env` file:

```bash
MONGODB_URI=mongodb+srv://your_username:your_password@cluster_url
GOOGLE_API_KEY=your_gemini_api_key
```

Start the app:

```bash
streamlit run app.py
```

</details>

## Usage

1. Upload candidate resumes and job descriptions to the database.
2. Select a job from the dropdown menu in the UI.
3. Click the "Match Candidates" button to generate scores and comments.
4. View the ranked list of candidates based on their match scores.

## Project structure

```text
app.py          Streamlit entry point and navigation (Jobs / Candidates / Matching)
jobs.py         Job description pages
candidates.py   Candidate resume pages and upload
matching.py     Matching page and ranking
gemini.py       Gemini extraction/comments and embedding-based match score
database.py     MongoDB connection and demo-mode in-memory database
demo_data.py    Sample data and keyword scoring for demo mode
loadfile.py     Resume file loading
docs/screenshots/   README screenshots
```

## Roadmap

- Add more advanced matching algorithms (e.g. BERT embeddings).
- Enhance UI for uploading resumes and job descriptions directly.
- Add user authentication for secure access.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Google Generative AI (Gemini API), MongoDB and Streamlit.
