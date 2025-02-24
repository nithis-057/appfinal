import streamlit as st
import fitz  # PyMuPDF
import docx
import google.generativeai as genai
import re

# Set up Gemini API Key
genai.configure(api_key="AIzaSyDJrBU_Q0hWvuw6wL_lI4EClmutjP4PW5I")

# Streamlit app title
st.set_page_config(page_title="Resume Optimizer")
st.title("Resume Optimizer")
st.write("Enhance your resume for ATS compatibility and your desired job role.")

# Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join([page.get_text("text") for page in doc])
    return text

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def clean_text(text):
    text = re.sub(r'[*-]+', '', text)  # Remove markdown symbols
    return text.strip()

def optimize_resume_gemini(resume_text, job_role):
    prompt = f"""
    Optimize my resume by improving clarity, readability, and keyword relevance for {job_role}. 
    Ensure the content is ATS-friendly by incorporating relevant industry-specific keywords naturally. 
    Enhance bullet points to be more action-oriented and results-driven, 
    using strong verbs and quantifiable achievements where possible. 
    Keep the formatting concise and professional while improving overall flow. 
    
    
    Here is my resume content: 
    {resume_text}
    
    
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error generating resume."

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file format!")
        resume_text = ""

    if resume_text:
        st.subheader("Extracted Resume Text")
        st.text_area("", resume_text, height=250)
        
        job_role = st.text_input("Target Job Role", "Software Engineer")
        
        if st.button("Optimize Resume"):
            with st.spinner("Enhancing your resume with AI..."):
                optimized_resume = optimize_resume_gemini(resume_text, job_role)
                
                st.subheader("Optimized Resume")
                st.text_area("", optimized_resume, height=250)
