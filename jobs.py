import streamlit as st
from datetime import datetime
import time
import loadfile as lf
import gemini as gemini
import database as database
from loadfile import refresh_page

def display_jobs():
    st.subheader("Job Descriptions")

    # Retrieve job descriptions from the database
    with st.spinner("Loading jobs..."):
        try:
            jobs = list(database.db.jobs.find({}, {"_id": 1, "position_name": 1, "short_description": 1, "created_date": 1}))
        except Exception as e:
            st.error(f"Error loading jobs: {e}")
            upload_new_job()  # Ensure upload is available even if there's an error
            return

    # If there are no jobs, display a message and show the upload section
    if not jobs:
        st.info("No job descriptions available. Please upload a job description.")
        upload_new_job()
        return

    # Define number of items per page
    items_per_page = 5
    total_jobs = len(jobs)
    total_pages = (total_jobs - 1) // items_per_page + 1

    # Page selection
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_jobs = jobs[start_idx:end_idx]

    # Display headers for the columns
    col1, col2, col3, col4 = st.columns([1, 3, 8, 4])
    with col1:
        st.write("**#**")
    with col2:
        st.write("**Position Name**")
    with col3:
        st.write("**Short Description**")
    with col4:
        st.write("**Actions**")

    # Display jobs for the current page
    for index, row in enumerate(current_jobs, start=start_idx + 1):
        col1, col2, col3, col4 = st.columns([1, 3, 8, 4])
        with col1:
            st.write(f"{index}")

        # Check if position_name and short_description exist and are not None
        position_name = row.get('position_name', 'N/A') if row.get('position_name') else 'N/A'
        short_description = row.get('short_description', 'No description available.') if row.get('short_description') else 'No description available.'

        with col2:
            st.write(position_name.split('.')[0])  # Use the first part of the name if it contains a '.'
        with col3:
            st.text_area("Job Description", short_description, height=150, key=f"desc_{index}")
        with col4:
            handle_job_buttons(row, index)

    # Upload or write a new job description
    upload_new_job()


def display_job_details():
    if 'selected_job_id' in st.session_state and st.session_state.show_job_details:
        with st.spinner("Loading job details..."):
            job_details = database.db.jobs.find_one({"_id": st.session_state.selected_job_id})
        
        if st.session_state.is_update:
            # Show update form if in update mode
            st.markdown("---")
            st.markdown("### Update Job Description")
            if job_details:
                position_name = st.text_input("Position Name", value=job_details['position_name'])
                job_description = st.text_area("Job Description", value=job_details['description'], height=150)
                education = st.text_area("Education", value=job_details['education'], height=100)
                experience = st.text_area("Experience", value=job_details['experience'], height=100)
                responsibilities = st.text_area("Responsibilities", value=job_details['responsibilities'], height=100)
                technical_skills = st.text_area("Technical Skills", value=job_details['technical skills'], height=100)
                soft_skills = st.text_area("Soft Skills", value=job_details['soft skills'], height=100)
                certifications = st.text_area("Certifications", value=job_details['certifications'], height=100)
                
                with st.container():
                    if st.button("Save Changes"):
                        try:
                            with st.spinner("Updating job description..."):
                                # Update the job data in the database
                                database.db.jobs.update_one({"_id": st.session_state.selected_job_id}, {"$set": {
                                    "position_name": position_name,
                                    "description": job_description,
                                    "education": education,
                                    "experience": experience,
                                    "responsibilities": responsibilities,
                                    "technical_skills": technical_skills,
                                    "soft_skills": soft_skills,
                                    "certifications": certifications,
                                    "created_date": datetime.now().strftime('%d-%m-%Y')
                                }})
                            st.success("Job Description Updated Successfully")
                            time.sleep(1)
                            refresh_page()
                        except Exception as e:
                            st.error(f"Error updating job description: {e}")

                    if st.button("Close Details"):
                        st.session_state.show_job_details = False
                        st.session_state.selected_job_id = None
                        refresh_page()
        else:
            # Show job details if not in update mode
            if job_details:
                st.markdown("### **Job Details**")
                st.markdown(f"**Job Name** - {job_details['position_name'].split('.')[0]}")
                st.write(f"**Job Description:** {job_details['description']}")
                education = job_details.get('education', 'N/A').splitlines()
                experience = job_details.get('experience', 'N/A').splitlines()
                responsibilities = job_details.get('responsibilities', 'N/A').splitlines()
                certifications = job_details.get('certifications', 'N/A').splitlines()
                technical_skills = job_details.get('technical_skills', 'N/A').splitlines()
                soft_skills = job_details.get('soft_skills', 'N/A').splitlines()
                
                # Display skills display
                lf.display_field("Education", education)
                lf.display_field("Experience", experience)
                lf.display_field("Responsibilities", responsibilities)
                lf.display_field("Technical Skills", technical_skills)
                lf.display_field("Soft Skills", soft_skills)
                lf.display_field("Certifications", certifications)
        
                st.write(f"**Created Date:** {job_details['created_date']}")

                # Delete and Close buttons
                with st.container():
                    if st.button("Close Details"):
                        st.session_state.show_job_details = False
                        st.session_state.selected_job_id = None
                        refresh_page()
    else:
        st.write("")

def upload_new_job():
    st.markdown("### Upload or Write Job Description")

    # Initialize session state variables for file and textarea usage
    if 'use_file' not in st.session_state:
        st.session_state.use_file = False
    if 'use_textarea' not in st.session_state:
        st.session_state.use_textarea = False

    # File uploader (only enabled if text area is not in use)
    if not st.session_state.use_textarea:
        uploaded_job = st.file_uploader('Upload Job Description:', type=['pdf', 'docx'], 
                                        key="job_file_uploader", 
                                        on_change=lambda: lf.set_input_type('file'))

    # Text area for job description (only enabled if file uploader is not in use)
    if not st.session_state.use_file:
        job_description_text = st.text_area("Or write the job description here:", 
                                            on_change=lambda: lf.set_input_type('textarea'))

    # Submit and Cancel buttons
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        if st.button('Submit Job Description'):
            with st.spinner("Submitting job description..."):
                try:
                    handle_job_submission(uploaded_job if st.session_state.use_file else None, 
                                        job_description_text if st.session_state.use_textarea else None)
                except Exception as e:
                    st.error(f"Error submitting job description: {e}")
    with col2:
        if st.button('Cancel'):
            lf.cancel_input()  # Clear input and refresh the page

    # Automatically reset usage state if user clears the file upload or text area
    if st.session_state.use_file and not uploaded_job:
        lf.cancel_input()
    if st.session_state.use_textarea and not job_description_text:
        lf.cancel_input()
      
def handle_job_submission(uploaded_job, job_description_text):
    with st.spinner("Processing job submission..."):
        if uploaded_job:
            if uploaded_job.type == 'application/pdf':
                job_description = lf.extract_text_from_file(uploaded_job)
            elif uploaded_job.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                job_description = lf.extract_text_from_file(uploaded_job)
            else:
                st.error("Unsupported file format")
                return
        elif job_description_text:
            job_description = job_description_text
        else:
            st.error("Please provide either a file or a description")
            return

    job_data = {
        "position_name": lf.format_name(gemini.format_gemini_job_title(job_description)),  
        "description": gemini.format_gemini_description(job_description),
        "short_description": gemini.format_gemini_short_description(job_description),
        "education": gemini.format_gemini_education_requirements(job_description),  
        "experience": gemini.format_gemini_experience(job_description),  
        "responsibilities": gemini.format_gemini_responsibilities(job_description),  
        "technical_skills": gemini.format_gemini_technical_skills(job_description),  
        "soft_skills": gemini.format_gemini_soft_skills(job_description),  
        "certifications": gemini.format_gemini_certifications(job_description),    
        "created_date": datetime.now().strftime('%d-%m-%Y')
    }

    try:
        with st.spinner("Uploading job description..."):
            # Save the job data to MongoDB
            database.db.jobs.insert_one(job_data)
        st.success("Job Description Uploaded Successfully")
        time.sleep(1)
        refresh_page()
    except Exception as e:
        st.error(f"Error uploading job description: {e}")

def handle_job_buttons(row, index):
    # Stack buttons vertically
    with st.container():
        # Detail button
        if st.button("Detail", key=f"detail_{index}", use_container_width=True):
            st.session_state.show_job_details = True
            st.session_state.selected_job_id = row['_id']
            st.session_state.is_update = False  # Reset update flag

        # Update button
        if st.button("Update", key=f"update_{index}", use_container_width=True):
            st.session_state.show_job_details = True
            st.session_state.selected_job_id = row['_id']
            st.session_state.is_update = True  # Set update flag

        # Delete button
        if st.button("Delete", key=f"delete_{index}", use_container_width=True):
            delete_job(row)

def update_job(row):
    st.markdown("### Update Job Description")
    
    try:
        job_data = database.db.jobs.find_one({"_id": row['_id']})
        if not job_data:
            st.error("Job not found in the database.")
            return
    except Exception as e:
        st.error(f"Error fetching job data: {e}")
        return

    if job_data:
        position_name = st.text_input("Position Name", value=job_data['position_name'])
        job_description = st.text_area("Job Description", value=job_data['description'], height=150)
        education = st.text_area("Education", value=job_data['education'], height=100)
        experience = st.text_area("Experience", value=job_data['experience'], height=100)
        responsibilities = st.text_area("Responsibilities", value=job_data['responsibilities'], height=100)
        technical_skills = st.text_area("Technical Skills", value=job_data['technical_skills'], height=100)
        soft_skills = st.text_area("Soft Skills", value=job_data['soft_skills'], height=100)
        certifications = st.text_area("Certifications", value=job_data['certifications'], height=100)

        with st.container():
            if st.button("Save Changes"):
                try:
                    with st.spinner("Updating job description..."):
                        database.db.jobs.update_one({"_id": row['_id']}, {"$set": {
                            "position_name": position_name,
                            "description": job_description,
                            "education": education,
                            "experience": experience,
                            "responsibilities": responsibilities,
                            "technical skills": technical_skills,
                            "soft skills": soft_skills,
                            "certifications": certifications,
                            "created_date": datetime.now().strftime('%d-%m-%Y')
                        }})
                    st.success("Job Description Updated Successfully")
                    time.sleep(1)
                    refresh_page()
                except Exception as e:
                    st.error(f"Error updating job description: {e}")
            if st.button("Cancel"): 
                refresh_page()

def delete_job(row):
    try:
        with st.spinner("Deleting job..."):
            database.db.jobs.delete_one({"_id": row['_id']})
        st.success("Job Deleted Successfully")
        time.sleep(1)
        refresh_page()
    except Exception as e:
        st.error(f"Error deleting job: {e}")
