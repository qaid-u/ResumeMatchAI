import os
import google.generativeai as genai
from functools import lru_cache
from regex import F
from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F

# Initialize a BERT-based model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
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

# Function to generate BERT embeddings
def get_bert_embeddings(text):
    try:
        return model.encode([text])[0]
    except Exception as e:
        print(f"Error generating BERT embeddings: {e}")
        return None

# Enhanced match score function using cosine similarity
def enhanced_match_score(resume_text, job_text):
    try:
        # Validate inputs
        if not resume_text or not job_text:
            print("Empty input detected.")
            return 0.0

        # Generate embeddings
        resume_embedding = get_bert_embeddings(resume_text)
        job_embedding = get_bert_embeddings(job_text)

        if resume_embedding is None or job_embedding is None:
            print("Failed to generate embeddings.")
            return 0.0

        # Calculate similarity
        similarity_score = calculate_cosine_similarity(resume_embedding, job_embedding)
        print(f"Cosine Similarity: {similarity_score}")

        # Scale similarity score
        match_score = round(similarity_score * 100, 2)
        return match_score

    except Exception as e:
        print(f"Error in enhanced match score calculation: {e}")
        return 0.0

def calculate_cosine_similarity(vec1, vec2):
    vec1 = torch.tensor(vec1, dtype=torch.float32)
    vec2 = torch.tensor(vec2, dtype=torch.float32)
    similarity = F.cosine_similarity(vec1.unsqueeze(0), vec2.unsqueeze(0))
    return similarity.item()