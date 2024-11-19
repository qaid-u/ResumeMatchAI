import time
import os
from turtle import st
from pymongo import MongoClient
from dotenv import load_dotenv
from gridfs import GridFS

from loadfile import refresh_page

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URI from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")

# Configure MongoDB connection
client = MongoClient(MONGODB_URI)
db = client['resume_match_ai']
fs = GridFS(db)

def ensure_collections():
    """Ensure that required collections exist."""
    # Ensures that 'jobs' and 'candidates' collections are created if not present
    if 'jobs' not in db.list_collection_names():
        db.create_collection('jobs')
    if 'candidates' not in db.list_collection_names():
        db.create_collection('candidates')

def insert_job(job_data):
    """Insert a new job description into the 'jobs' collection."""
    db.jobs.insert_one(job_data)

def update_job(job_id, updated_data):
    """Update an existing job description in the 'jobs' collection."""
    with st.spinner("Deleting job..."):
        try:
            db.jobs.update_one({"_id": job_id}, {"$set": updated_data})
            st.success("Job Updated Successfully")
            time.sleep(1)
            refresh_page()
        except Exception as e:
            st.error(f"Error updating job: {e}")

def delete_job(job_id):
    """Delete a job description from the 'jobs' collection."""
    with st.spinner("Deleting job..."):
        try:
            db.jobs.delete_one({"_id": job_id})
            st.success("Job Deleted Successfully")
            time.sleep(1)
            refresh_page()
        except Exception as e:
            st.error(f"Error deleting job: {e}")

def get_all_jobs():
    """Retrieve all job descriptions."""
    return list(db.jobs.find({}, {"_id": 1, "position_name": 1, "short_description": 1, "created_date": 1}))

def get_job_details(job_id):
    """Retrieve detailed information for a specific job description."""
    return db.jobs.find_one({"_id": job_id})

def insert_candidate(candidate_data):
    """Insert a new candidate resume into the 'candidates' collection."""
    db.candidates.insert_one(candidate_data)

def get_all_candidates():
    """Retrieve all candidate resumes."""
    return list(db.candidates.find({}, {"_id": 1, "name": 1, "summary": 1, "uploaded_date": 1}))

def get_candidate_details(candidate_id):
    """Retrieve detailed information for a specific candidate resume."""
    return db.candidates.find_one({"_id": candidate_id})
