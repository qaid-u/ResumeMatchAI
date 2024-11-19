import os
import google.generativeai as genai
from functools import lru_cache

cache = {}

@lru_cache(maxsize=None)
def get_gemini_response(input_text, model_name="models/gemini-1.5-flash-001"):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        # Use the generation configuration when calling the generate_content method
        response = model.generate_content(input_text)
        # Return the response text
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None
    
# Job Description Formatting Functions
def format_gemini_short_description(job_text):
    prompt = f"""
    Job Description: {job_text}
    Please provide a concise and accurate summary of the job description based on the following details:
    - Education Requirements: (List the education qualifications needed for this role)
    - Work Experience Requirements: (Provide the years and type of experience needed)
    - Responsibilities: (Highlight the key responsibilities in bullet points)
    - Technical Skills: (List specific technical skills required)
    - Soft Skills: (Mention the interpersonal or communication skills desired)
    - Certifications: (Mention any specific certifications required or preferred)
    Provide your summary as a single well-structured paragraph that clearly captures the main aspects of the job.
    """
    return get_gemini_response(prompt)

def format_gemini_description(text):
    prompt = f"""
    Job Description: {text}
    Please generate a short and compact summary of this job description.
    The summary should be succinct yet informative, covering the most important points in one concise paragraph.
    """
    return get_gemini_response(prompt)

# Resume Information Extraction Functions
def format_gemini_name(text):
    prompt = f"""
    Resume: {text}
    Please extract the full name or name of the person listed in the resume. Ensure the name is formatted correctly with the first and last names. If there is no full name listed, use the best available name. Output the name only.
    """
    return get_gemini_response(prompt)

def format_gemini_job_title(text):
    prompt = f"""
    Text: {text}
    Please extract the job title in the text. Ensure the job title is formatted correctly. Output the job title only.
    """
    return get_gemini_response(prompt)

def format_gemini_email_address(text):
    prompt = f"""
    Resume: {text}
    Please extract the email address of the individual from the resume. Ensure the email address is in proper format and complete. Output the email address only. Ensure it is the resume owner's email address by similarity to the owner's name.
    """
    return get_gemini_response(prompt)

def format_gemini_phone_number(text):
    prompt = f"""
    Resume: {text}
    Please extract the mobile phone number of the individual from the resume. The number should be complete and properly formatted. Output the phone number only. Use +60 format for Malaysian numbers.
    """
    return get_gemini_response(prompt)

def format_gemini_summary(text):
    prompt = f"""
    Resume: {text}
    Please generate a summary of the candidate’s resume. Highlight the key skills, experience, and qualifications. Output the summary only.
    """
    return get_gemini_response(prompt)

# Resume Details Extraction Functions
def format_gemini_education(text):
    prompt = f"""
    Text: {text}
    Please extract all educational and degree levels mentioned in this text. Provide them as a list of bullet points, including any specific degrees (e.g., Bachelor's, Master's, PhD) or certifications (e.g., High School Diploma, Professional Certification). If no educational qualifications are mentioned, simply return 'none'. Output the list only.
    """
    return get_gemini_response(prompt)

def format_gemini_education_requirements(text):
    prompt = f"""
    Job Description: {text}
    Please extract all educational and degree levels mentioned in this text. Provide them as a list of bullet points, including any specific degrees (e.g., Bachelor's, Master's, PhD) or certifications (e.g., High School Diploma, Professional Certification). If no educational qualifications are mentioned, simply return 'none'. Output the list only. Output the full degree name.
    Note:
    - Interpret 'or' as alternative options.
    - Interpret 'and' as required inclusions.
    - Treat '/' and '&' as different ways to indicate equivalent or interchangeable terms.
    """
    return get_gemini_response(prompt)

def format_gemini_experience(text):
    prompt = f"""
    Text: {text}
    Please extract the required work experience from this text. List the following details:
    - The number of years of experience required (e.g., 3 years, 5+ years).
    - The specific type(s) of work experience or skills needed (e.g., software development, project management, customer service). Output the list only.
    If no work experience is mentioned, simply return 'none'.
    """
    return get_gemini_response(prompt)

def format_gemini_responsibilities(text):
    prompt = f"""
    Text: {text}
    Please extract the key responsibilities listed in this text. For each responsibility, include the main task or duty expected from the role. Present each responsibility as a bullet point, ensuring it is brief, clear, and action-oriented (e.g., "Manage team projects," "Develop software solutions"). If no responsibilities are mentioned, simply return 'none'. Output the list only.
    """
    return get_gemini_response(prompt)

def format_gemini_technical_skills(text):
    prompt = f"""
    Text: {text}
    Please extract all technical skills mentioned in this text. Include specific tools, programming languages, software, platforms, or technical expertise. List them as bullet points, without any titles or introductory text. Ensure that each skill is distinct and precise (e.g., Python, JavaScript, AWS, SQL, Git). If no technical skills are mentioned, simply return 'none'. Output the list only.
    """
    return get_gemini_response(prompt)

def format_gemini_soft_skills(text):
    prompt = f"""
    Text: {text}
    Please extract all soft skills mentioned in this text. Soft skills include interpersonal abilities, communication skills, problem-solving, leadership qualities, teamwork, and other non-technical attributes. List each skill in bullet points, ensuring clarity and precision. If no soft skills are mentioned, simply return 'none'. Output the list only.
    """
    return get_gemini_response(prompt)

def format_gemini_certifications(text):
    prompt = f"""
    Text: {text}
    Please extract all certifications mentioned in this text. This includes professional certifications, licenses, and any formal qualifications that are recognized in a specific field or industry (e.g., PMP, AWS Certified Solutions Architect, Microsoft Certified). List each certification in bullet points, ensuring that each one is distinct and accurate. If no certifications are mentioned, simply return 'none'. Output the list only.
    """
    return get_gemini_response(prompt)

# Match Score and Comment Generation Functions
def gemini_generate_match_score(resume_text, job_text):
    # Create a unique key based on resume and job text
    prompt_key = f"match_score:{resume_text}:{job_text}"
    
    # Check if the response is already cached
    if prompt_key in cache:
        return cache[prompt_key]
    
    # Create the prompt
    prompt = f"""
    Resume: {resume_text}
    Job Description: {job_text}
    Please generate a match score between 0 and 100 based on the similarity between the resume and the job description. Only number. The score is based on the order for most important aspects: technical skills, responsibilities, experience, education, soft skills, and least is certifications. Output the score only.
    """
    
    # Generate response and store in cache
    response = get_gemini_response(prompt)
    cache[prompt_key] = response
    return response

def gemini_generate_comment(resume_text, job_text):
    # Create a unique key based on resume and job text
    prompt_key = f"comment:{resume_text}:{job_text}"
    
    # Check if the response is already cached
    if prompt_key in cache:
        return cache[prompt_key]
    
    # Create the prompt
    prompt = f"""
    Resume: {resume_text}
    Job Description: {job_text}
    Please generate a comment based on the similarity between the resume and the job description. Ensure the comment is in one short paragraph that is specific and informative. Output the comment only.
    """
    
    # Generate response and store in cache
    response = get_gemini_response(prompt)
    cache[prompt_key] = response
    return response