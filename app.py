import streamlit as st
from dotenv import load_dotenv
import database
import jobs as jobs 
import candidates as candidates
import matching as matching

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    st.error(f"Error loading environment variables: {e}")

# Sidebar layout for section selection
st.sidebar.header('ResumeMatchAI')

# Ensure collections exist
try:
    database.ensure_collections()
except Exception as e:
    st.error(f"Database initialization error: {e}")

# Initialize the selected section in session state if it’s not already set
if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Jobs"  # Default section

# Buttons for section selection
if st.sidebar.button("Jobs"):
    st.session_state.selected_section = "Jobs"
if st.sidebar.button("Candidates"):
    st.session_state.selected_section = "Candidates"
if st.sidebar.button("Matching"):
    st.session_state.selected_section = "Matching"

# Render selected section content based on session state
try:
    if st.session_state.selected_section == "Jobs":
        try:
            jobs.display_jobs()
            jobs.display_job_details()
        except Exception as e:
            st.error(f"Error displaying jobs: {e}")
            
    elif st.session_state.selected_section == "Candidates":
        try:
            candidates.display_candidates()
        except Exception as e:
            st.error(f"Error displaying candidates: {e}")
            
    elif st.session_state.selected_section == "Matching":
        try:
            matching.display_matching_table()
        except Exception as e:
            st.error(f"Error displaying matching table: {e}")

except Exception as main_e:
    st.error(f"An unexpected error occurred: {main_e}")
