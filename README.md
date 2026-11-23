# ResumeMatchAI  
An AI-powered tool for matching resumes to job descriptions using the Gemini API. This system utilizes NLP to analyze and rank candidates based on key job criteria like technical skills, experience, education, and certifications. Built with Streamlit for the user interface and MongoDB for data storage.  

## Features  
- **AI Matching**: Leverages the Gemini API to score candidates based on their suitability for a job description.  
- **Candidate Ranking**: Automatically sorts candidates by match score for easy comparison.  
- **Detailed Feedback**: Provides a summary and comment for each candidate based on their match.  
- **Streamlit UI**: Simple and interactive interface for selecting jobs and viewing ranked candidates.  
- **MongoDB Integration**: Stores candidate resumes, job descriptions, and matching results.  

## Technologies Used  
- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: MongoDB  
- **API**: Gemini API (Google Generative AI)  

## Preview

![Jobs](docs/screenshots/jobs.png)

| Candidates | Matching results |
|---|---|
| ![Candidates](docs/screenshots/candidates.png) | ![Matching results](docs/screenshots/matching-results.png) |

### Try it without any setup (demo mode)
The app runs in **demo mode** whenever `MONGODB_URI` is not set (or `DEMO_MODE=1`). It uses an in-memory database seeded with fictional jobs and candidates, and scores matches by keyword overlap instead of calling Gemini, so no database, API key or ML models are needed.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Uploading jobs and resumes is disabled in demo mode, since it needs Gemini and OCR.

### Host the demo for free
1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **Create app**, pick this repo, branch `main`, main file `app.py`.
3. Deploy, without setting any secrets, so it starts in demo mode.
4. Add the resulting URL here as a "Live demo" link.

## Installation  
### Prerequisites  
- Python 3.8+
- Tesseract OCR (for scanned PDFs) and the spaCy model: `python -m spacy download en_core_web_sm`  
- MongoDB database (cloud or local)  
- API key for the Gemini API  

### Steps  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/qaid-u/ResumeMatchAI.git  
   cd ResumeMatchAI  
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv  
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements-full.txt  
   ```
4. Setup your .env file with the following:
   ```bash
   MONGODB_URI=mongodb+srv://your_username:your_password@cluster_url  
   GOOGLE_API_KEY=your_gemini_api_key
5. Start the Streamlit app:
   ```bash
   streamlit run app.py  
   ```

### Usage
1. Upload candidate resumes and job descriptions to the database.
2. Select a job from the dropdown menu in the UI.
3. Click the "Match Candidates" button to generate scores and comments.
4. View the ranked list of candidates based on their match scores.

### Roadmap
- Add more advanced matching algorithms (e.g., cosine similarity, BERT embeddings).
- Enhance UI for uploading resumes and job descriptions directly.
- Add user authentication for secure access.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments
- Google Generative AI for the Gemini API.
- MongoDB for database solutions.
- Streamlit for the interactive UI framework.
