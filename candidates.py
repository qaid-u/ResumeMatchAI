import base64
import streamlit as st
from datetime import datetime
import pandas as pd
import loadfile as lf
import gemini
import time
import database
from loadfile import refresh_page

def display_candidates():
    st.markdown("### Upload Candidate Resumes")
    
    # Enable multiple file uploads
    uploaded_resumes = st.file_uploader('Upload Candidate Resumes:', type=['pdf', 'docx'], accept_multiple_files=True)

    if uploaded_resumes:
        # Handle file submission
        if st.button('Submit Resumes'):
            handle_resume_submission(uploaded_resumes)

    st.markdown("### Candidate Resumes")
    
    # Retrieve candidates from MongoDB and display
    candidates = list(database.db.candidates.find({}, {
        "_id": 1,
        "name": 1,
        "email_address": 1,
        "phone_number": 1,
        "uploaded_date": 1,
        "education": 1,
        "file_data": 1,
        "file_name": 1,
        "file_type": 1,
        "experience": 1,
        "technical_skills": 1,
        "soft_skills": 1,
        "certifications": 1,
        "summary": 1,
    }))

    # Check if any candidates are retrieved
    if not candidates:
        st.warning("No candidates found. Please add resumes.")
        return

    # If candidates exist, proceed with pagination and display
    candidates_per_page = 5
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0

    # Paginate candidates
    start_idx = st.session_state.current_page * candidates_per_page
    end_idx = start_idx + candidates_per_page
    page_candidates = candidates[start_idx:end_idx]

    render_candidate_table(page_candidates)
    render_navigation_controls(candidates, candidates_per_page)

    # Render detailed view if selected
    if st.session_state.get("show_candidate_details", False):
        selected_candidate_id = st.session_state.get("selected_candidate_id")
        candidate_details = next((candidate for candidate in candidates if candidate["_id"] == selected_candidate_id), None)
        if candidate_details:
            render_candidate_details(candidate_details)
        else:
            st.warning("No candidate details found for the selected candidate ID.")

def render_candidate_details(candidate_details):
    """Render detailed view for selected candidate."""
    st.markdown("---")
    st.markdown("### **Candidate Details**")

    # Display general details
    st.write(f"**Name:** {candidate_details.get('name', 'N/A').split('.')[0].title()}")
    st.write(f"**Email Address:** {candidate_details.get('email_address', 'N/A')}")
    st.write(f"**Phone Number:** {candidate_details.get('phone_number', 'N/A')}")
    education = candidate_details.get('education', 'N/A').splitlines()
    experience = candidate_details.get('experience', 'N/A').splitlines()
    certifications = candidate_details.get('certifications', 'N/A').splitlines()
    technical_skills = candidate_details.get('technical_skills', 'N/A').splitlines()
    soft_skills = candidate_details.get('soft_skills', 'N/A').splitlines()

    # Display Education with formatting
    st.markdown("**Education:**")
    if education and education[0] != "N/A":
        for skill in education:
            st.markdown(f"- {skill.strip()}")
    else:
        st.write("N/A")

    # Display Experience with formatting
    st.markdown("**Experience:**")
    if experience and experience[0] != "N/A":
        for skill in experience:
            st.markdown(f"- {skill.strip()}")
    else:
        st.write("N/A")

    st.write(f"**Summary:** {candidate_details.get('summary', 'N/A')}")

    st.markdown("**Technical Skills:**")
    if technical_skills and technical_skills[0] != "N/A":
        for skill in technical_skills:
            st.markdown(f"- {skill.strip()}")
    else:
        st.write("N/A")

    # Display Soft Skills with formatting
    st.markdown("**Soft Skills:**")
    if soft_skills and soft_skills[0] != "N/A":
        for skill in soft_skills:
            st.markdown(f"- {skill.strip()}")
    else:
        st.write("N/A")

    st.markdown("**Certifications:**")
    if certifications and certifications[0] != "N/A":
        for skill in certifications:
            st.markdown(f"- {skill.strip()}")
    else:
        st.write("N/A")
    
    st.write(f"**Uploaded Date:** {candidate_details.get('uploaded_date', 'N/A')}")

    # Display Preview button
    if st.button("Preview Resume"):
        file_data = candidate_details.get('file_data', b'')
        file_type = candidate_details.get('file_type', 'application/pdf')

        # Handle file preview (only PDF supported here)
        if file_type == "application/pdf" and file_data:
            try:
                # Make sure the file_data is a byte string and decode it from base64
                if isinstance(file_data, str):
                    # If the file_data is a string, decode it from base64
                    file_data = base64.b64decode(file_data.split('base64,')[1])

                # Now that file_data is decoded, create the URL
                pdf_url = f"data:application/pdf;base64,{base64.b64encode(file_data).decode()}"

                # Embed the PDF in an iframe using HTML
                st.markdown(f'<iframe src="{pdf_url}" width="700" height="600"></iframe>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error displaying the PDF: {e}")
        else:
            st.write("Preview not available for this file type or no file data provided.")
    
    # Ensure that "Close Details" button stays visible
    if st.button("Close Details"):
        st.session_state.show_candidate_details = False
        st.session_state.selected_candidate_id = None
        refresh_page()


def render_candidate_table(candidates):
    """Render the candidate list in a table-like format."""
    candidate_data = pd.DataFrame(candidates)
    candidate_data.index = candidate_data.index + 1

    # Define columns for display
    col1, col2, col3, col4, col5, col6 = st.columns([1, 8, 8, 8, 7, 7])
    with col1: st.markdown("**#**")
    with col2: st.markdown("**Name**")
    with col3: st.markdown("**Email Address**")
    with col4: st.markdown("**Phone Number**")
    with col5: st.markdown("**Uploaded Date**")
    with col6: st.markdown("**Actions**")

    # Render each row
    for index, row in candidate_data.iterrows():
        render_candidate_row(index, row)

def render_candidate_row(index, row):
    """Render a single row for a candidate."""
    col1, col2, col3, col4, col5, col6 = st.columns([1, 8, 8, 8, 7, 7])
    
    with col1:
        st.write(f"{index}")
    with col2:
        candidate_name = lf.format_name(row['name'])
        st.write(candidate_name)
    with col3:
        st.write(f"{row.get('email_address', 'N/A')}")
    with col4:
        st.write(f"{row.get('phone_number', 'N/A')}")
    with col5:
        st.write(f"{row.get('uploaded_date', 'N/A')}")
    with col6:
        render_candidate_actions(index, row)

def render_candidate_actions(index, row):
    """Render action buttons for each candidate row."""
    # Detail button
    if st.button("Detail", key=f"candidate_detail_{index}", use_container_width=True):
        st.session_state.show_candidate_details = True
        st.session_state.selected_candidate_id = row['_id']
        # Trigger scroll to job details
        st.session_state.scroll_to_job_details = True
    
    # Delete button
    if st.button("Delete", key=f"candidate_delete_{index}", use_container_width=True):
        delete_candidate(row['_id'])
    
    # Download button
    st.download_button(
        label="Download",
        data=row['file_data'],
        file_name=row['file_name'],
        mime=row['file_type'],
        key=f"candidate_download_{index}",
        use_container_width=True
    )


def render_navigation_controls(candidates, candidates_per_page):
    """Render navigation controls for pagination."""
    total_pages = (len(candidates) // candidates_per_page) + (1 if len(candidates) % candidates_per_page > 0 else 0)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.current_page > 0 and st.button('Previous', key='prev_page'):
            st.session_state.current_page -= 1
    
    with col2:
        st.write(f"Page {st.session_state.current_page + 1} of {total_pages}")
    
    with col3:
        if st.session_state.current_page < total_pages - 1 and st.button('Next', key='next_page'):
            st.session_state.current_page += 1


# Function to handle resume submissions
def handle_resume_submission(uploaded_resumes):
    """Handle multiple resume submissions: extract content, process, and store each in the database."""
    failed_files = []  # Track failed submissions
    success_files = []  # Track successful submissions
    
    for uploaded_resume in uploaded_resumes:
        if uploaded_resume:
            with st.spinner(f"Processing {uploaded_resume.name}..."):
                # Extract text from the file based on its extension
                extracted_text = lf.extract_text_from_file(uploaded_resume)
                
                # Error handling for null extracted data
                if not extracted_text or extracted_text.strip() == "":
                    st.warning(f"Failed to extract meaningful content from {uploaded_resume.name}. Please check the file format and content.")
                    failed_files.append(uploaded_resume.name)
                    continue
                
                # Extract candidate details using Gemini processing functions with error handling
                try:
                    candidate_data = {
                        "name": gemini.format_gemini_name(extracted_text) or "N/A",
                        "email_address": gemini.format_gemini_email_address(extracted_text) or "N/A",
                        "phone_number": gemini.format_gemini_phone_number(extracted_text) or "N/A",
                        "summary": gemini.format_gemini_summary(extracted_text) or "N/A",
                        "education": gemini.format_gemini_education(extracted_text) or "N/A",
                        "experience": gemini.format_gemini_experience(extracted_text) or "N/A",
                        "technical_skills": gemini.format_gemini_technical_skills(extracted_text) or "N/A",
                        "soft_skills": gemini.format_gemini_soft_skills(extracted_text) or "N/A",
                        "certifications": gemini.format_gemini_certifications(extracted_text) or "N/A",
                        "uploaded_date": datetime.now().strftime('%d-%m-%Y'),
                        "file_data": uploaded_resume.getvalue(),  # Binary data for file download
                        "file_name": uploaded_resume.name,
                        "file_type": uploaded_resume.type
                    }
                except Exception as e:
                    st.error(f"Error processing candidate data from {uploaded_resume.name}: {e}")
                    failed_files.append(uploaded_resume.name)
                    continue

                # Store candidate data in MongoDB
                try:
                    database.db.candidates.insert_one(candidate_data)
                    success_files.append(uploaded_resume.name)
                except Exception as e:
                    st.error(f"Error storing candidate data in the database for {uploaded_resume.name}: {e}")
                    failed_files.append(uploaded_resume.name)
                    
    # Display results of the file processing
    if failed_files:
        st.warning(f"Files failed to process: {', '.join(failed_files)}.")
    if success_files:
        st.success(f"Files uploaded successfully: {', '.join(success_files)}.")

    # Refresh the page if all files processed successfully
    if success_files and not failed_files:
        time.sleep(1)
        refresh_page()


def delete_candidate(candidate_id):
    """Delete a candidate from the database."""
    with st.spinner("Deleting resume..."):
        database.db.candidates.delete_one({"_id": candidate_id})
    st.success("Candidate Resume Deleted Successfully")
    time.sleep(1)
    refresh_page()