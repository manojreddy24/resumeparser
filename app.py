import streamlit as st
import openai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API key
openai.api_key ="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"


# ChatGPT API function
def get_chatgpt_response(input_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Convert PDF to text
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Input prompt template
input_prompt_template = """
### As a skilled Application Tracking System (ATS) with advanced knowledge in technology and data science, your role is to meticulously evaluate a candidate's resume based on the provided job description. 

### Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for key buzzwords and specific criteria outlined in the job description to determine the candidate's suitability for the position.

### Provide a detailed assessment of how well the resume matches the job requirements, highlighting strengths, weaknesses, and any potential areas of concern. Offer constructive feedback on how the candidate can enhance their resume to better align with the job description and improve their chances of securing the position.

### Your evaluation should be thorough, precise, and objective, ensuring that the most qualified candidates are accurately identified based on their resume content in relation to the job criteria.

### Resume:
{text}

### Job Description:
{jd}

### Evaluation Output:
1. Calculate the percentage of match between the resume and the job description. Give a number and some explanation.
2. Identify any key keywords that are missing from the resume in comparison to the job description.
3. Offer specific and actionable tips to enhance the resume and improve its alignment with the job requirements.
"""

# Streamlit UI
st.title("DDS Smart ATS")
st.text("Improve your ATS resume score match")
jd = st.text_area("Paste job description here")
uploaded_file = st.file_uploader("Upload your resume", type="pdf", help="Please upload the PDF")

submit = st.button('Check Your Score')
if submit:
    if uploaded_file is not None and jd.strip():
        text = input_pdf_text(uploaded_file)
        prompt = input_prompt_template.format(text=text, jd=jd)
        response = get_chatgpt_response(prompt)
        st.subheader("Evaluation Output")
        st.write(response)
    else:
        st.error("Please upload a resume and provide a job description.")
