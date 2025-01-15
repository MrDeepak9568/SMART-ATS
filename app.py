import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Ensure you have a .env file with GOOGLE_API_KEY defined

# Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call GenAI
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt template
input_prompt_template = """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. Assign the percentage Matching based 
on JD and
the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

# Input fields
jd = st.text_area("Paste the Job Description", placeholder="Enter the job description here...")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF resume")

# Submit button logic
submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        # Extract text from the uploaded PDF
        resume_text = input_pdf_text(uploaded_file)
        
        # Format the input prompt
        formatted_prompt = input_prompt_template.format(text=resume_text, jd=jd)
        
        try:
            # Get the Gemini response
            response = get_gemini_response(formatted_prompt)
            st.subheader("AI Response")
            st.text(response)
        except Exception as e:
            st.error(f"Error generating response: {e}")
    else:
        st.error("Please provide both a job description and upload a resume.")
