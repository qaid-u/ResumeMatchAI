import streamlit as st
import pandas as pd
import database
import gemini  # Assuming `gemini` is a module for Gemini API functions
from bson import ObjectId  # Import to handle MongoDB Object IDs

def get_jobs():
    """Fetch job titles and IDs from the database for the dropdown."""
    try:
        jobs = database.db.jobs.find({}, {"_id": 1, "position_name": 1})
        return [{"id": str(job["_id"]), "position_name": job["position_name"]} for job in jobs]
    except Exception as e:
        st.error(f"Error fetching job titles: {e}")
        return []

def display_candidate_table():
    st.markdown("### Matching Candidate Resumes")
    
    try:
        candidates = list(database.db.candidates.find({}, {"_id": 1, "name": 1, "email_address": 1, "phone_number": 1, "uploaded_date": 1}))
        if candidates:
            candidate_data = pd.DataFrame(candidates)
            candidate_data.index += 1

            # Display selected fields in a structured table
            candidate_data = candidate_data[['name', 'email_address', 'phone_number', 'uploaded_date']]
            candidate_data['name'] = candidate_data['name'].str.title()
            candidate_data.rename(columns={
                'name': 'Name',
                'email_address': 'Email Address',
                'phone_number': 'Phone Number',
                'uploaded_date': 'Uploaded Date'
            }, inplace=True)
            st.dataframe(candidate_data, use_container_width=True, height=300)
        else:
            st.warning("No candidates found.")
    except Exception as e:
        st.error(f"Error displaying candidates: {e}")

def display_matching_table():
    display_candidate_table()
    jobs = get_jobs()
    
    if not jobs:
        st.warning("No job titles available to select.")
        return

    job_options = {job["position_name"]: job["id"] for job in jobs}
    selected_job_title = st.selectbox("Select Job", job_options.keys())
    selected_job_id = job_options.get(selected_job_title)
    
    if st.button("Match Candidates") and selected_job_id:
        with st.spinner("Processing candidate matching..."):
            try:
                matching_candidates_and_resume(selected_job_id)
                display_sorted_candidates()
            except Exception as e:
                st.error(f"Error matching candidates: {e}")

def matching_candidates_and_resume(job_id):
    try:
        # Retrieve all candidate details from the database
        candidates = list(database.db.candidates.find({}, {"_id": 1, "name": 1, "email_address": 1, "phone_number": 1, 
                                                           "uploaded_date": 1, "education": 1, "experience": 1, 
                                                           "technical_skills": 1, "soft_skills": 1, "responsibilities": 1, 
                                                           "certifications": 1}))
        
        # Fetch job description based on job ID
        job_description = database.db.jobs.find_one({"_id": ObjectId(job_id)})
        
        if job_description is None:
            st.warning(f"No job description found for job ID '{job_id}'")
            return

        # Extract job details with checks for each field
        job_data = {
            "position_name": job_description.get("position_name", ""),
            "description": job_description.get("description", ""),
            "short_description": job_description.get("short_description", ""),
            "technical_skills": job_description.get("technical_skills", "none"),
            "responsibilities": job_description.get("responsibilities", "none"),
            "experience": job_description.get("experience", "none"),
            "education": job_description.get("education", "none"),
            "soft_skills": job_description.get("soft_skills", "none"),
            "certifications": job_description.get("certifications", "none")
        }

        # Iterate over each candidate to compare their data with the job description
        for candidate in candidates:
            candidate_data = {
                "name": candidate.get("name", ""),
                "email_address": candidate.get("email_address", ""),
                "phone_number": candidate.get("phone_number", ""),
                "education": candidate.get("education", ""),
                "experience": candidate.get("experience", ""),
                "technical_skills": candidate.get("technical_skills", "").splitlines(),
                "soft_skills": candidate.get("soft_skills", "").splitlines(),
                "responsibilities": candidate.get("responsibilities", ""),
                "certifications": candidate.get("certifications", "")
            }

            try:
                # Calculate match score and generate comment
                match_score = gemini.gemini_generate_match_score(candidate_data, job_data)
                comment = gemini.gemini_generate_comment(candidate_data, job_data)
                
                # Update candidate's match score and comment in the database
                database.db.candidates.update_one({"_id": candidate["_id"]}, {"$set": {"match_score": match_score, "comment": comment}})
            
            except Exception as e:
                st.warning(f"Error calculating match score for {candidate.get('name', 'Unknown')}: {e}")

    except Exception as e:
        st.error(f"Error retrieving candidates for matching: {e}")

def display_sorted_candidates():
    st.markdown("### Matched Candidates Sorted by Score")

    try:
        # Retrieve candidates with a match score and associated details from the database
        candidates = list(
            database.db.candidates.find(
                {"match_score": {"$exists": True}}, 
                {"name": 1, "email_address": 1, "phone_number": 1, "match_score": 1, "comment": 1, "file_data": 1, "file_name": 1, "file_type": 1}
            )
        )
        
        # If no candidates are found with match scores, show a warning
        if not candidates:
            st.warning("No matched candidates found.")
            return

        # Sort candidates by their match score in descending order
        sorted_candidates = sorted(candidates, key=lambda x: x["match_score"], reverse=True)

        # Display each candidate's details in a card-like structure
        for candidate in sorted_candidates:
            with st.container():
                st.markdown("---")
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(candidate.get("name", "N/A").title())
                    st.write(f"**Email:** {candidate.get('email_address', 'N/A')}")
                    st.write(f"**Phone:** {candidate.get('phone_number', 'N/A')}")

                    short_comment = candidate.get("comment", "")
                    if short_comment:
                        # Show a shortened comment with a full view option in an expander
                        short_comment = short_comment[:100] + "..." if len(short_comment) > 100 else short_comment
                        st.write(f"**Comment:** {short_comment}")
                        with st.expander("Show full comment"):
                            st.write(candidate["comment"])
                    else:
                        st.write("**Comment:** No comment available.")

                with col2:
                    st.write(f"**Match Score:** {candidate.get('match_score', 'N/A')}")

                    # Provide a download button if 'file_data' is available for the candidate
                    file_data = candidate.get("file_data")
                    if file_data:
                        try:
                            st.download_button(
                                label="Download Resume",
                                data=file_data,  # Binary file data retrieved from MongoDB
                                file_name=candidate.get("file_name", "resume.pdf"),
                                mime=candidate.get("file_type", "application/pdf"),
                                use_container_width=True
                            )
                        except Exception as e:
                            st.write(f"Error retrieving file for {candidate.get('name', 'N/A')}: {e}")
                    else:
                        st.write("Resume file not available.")
                        
    except Exception as e:
        st.error(f"Error displaying sorted candidates: {e}")
