from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
import io
import base64

from PIL import Image
import pdf2image

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the pdf into image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),500,poppler_path=r'C:\Program Files (x86)\poppler\Library\bin')
        first_page = images[0]
        #convert into bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [{
            "mime_type": "image/jpeg",  # Corrected key name
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Streamlit data
st.set_page_config(page_title="ATS Resume Expert", page_icon=":rocket:")
st.header("Smart ATS Resume Tracker")
st.markdown("---")
input_text = st.text_area("Job Description : ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF) ...",type = ["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

# Buttons
col1, col2 = st.columns(2)
submit1 = col1.button("Percentage Match")
submit2 = col2.button("Tell me about the resume")

#submit1 = st.button("Percentage Match")

#submit2 = st.button("Tell me about the resume")

input_prompt1="""
You are an ATS(Application Tracking System) scanner with a deep understanding of any one job role from data science ,
full stack web development ,big data engineering ,devops, mlops, Artificial Intellience, machine learning 
and deep ATS functionality .Your task is to evaluate the resume against the provided job description and give
me the percentage of match if the resume matches the job description. First the output should come in percentage 
and then the keywords missing in resume only but are there in job description with high accuracy in a seperate line with 100 percent accuracy.
"""


input_prompt2="""
You are an experienced HR with technology experience in the field of any job role from data science,
 full stack web development ,big data engineering ,devops, mlops, Artificial Intellience, machine learning 
 your task is to review the provided resume against the job description for these profiles.
 Please share your professional evaluation on whether the candidate's profile aligns with the given job description
 Highlight the strengths and weaknesses of the applicant in relation to the specified job description
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Percentage Match & Keywords Missing:")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Professional Evaluation:")
        st.write(response)
    else:
        st.write("Please upload the resume")