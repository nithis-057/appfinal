import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai

# Set up Gemini API Key
genai.configure(api_key="AIzaSyDJrBU_Q0hWvuw6wL_lI4EClmutjP4PW5I")

# Streamlit app title
st.set_page_config(page_title="JD Matcher & Skill Gap Analysis", layout="wide")
st.title("JD Matcher & Skill Gap Analysis")
st.write("Upload your resume and get a detailed comparison with a job description.")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    try:
        with uploaded_file as f:
            pdf_data = f.read()
        
        doc = fitz.open(stream=pdf_data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# File uploader for resume
resume_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if resume_file is not None:
    with st.spinner("Extracting text from resume..."):
        resume_text = extract_text_from_pdf(resume_file)
        
        if not resume_text:
            st.error("⚠️ Could not extract text from the uploaded resume.")
        else:
            st.success("✅ Resume processed successfully!")
            st.text_area("Extracted Resume Content:", resume_text, height=300)

# Function to get job description from Gemini AI
def get_job_description(role):
    prompt = f"Generate a job description for a {role} role."
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error generating job description."

# User selects job role
job_role = st.text_input("Enter the Job Role", "Software Engineer")
if st.button("Generate Job Description"):
    with st.spinner("Fetching job description..."):
        job_desc = get_job_description(job_role)
        if not job_desc or "Error" in job_desc:
            st.error("Failed to generate job description. Try again.")
        else:
            st.session_state["job_desc"] = job_desc
            st.text_area("Generated Job Description:", job_desc, height=300)

# Skill gap analysis
def analyze_skill_gap(resume_text, job_desc):
    prompt = f"Compare the following resume text with the job description and provide a skill gap analysis:\n\nResume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\nHighlight missing skills and suggest improvements."
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Error analyzing skill gap."

if resume_file and "job_desc" in st.session_state:
    with st.spinner("Analyzing skill gaps..."):
        skill_gap_analysis = analyze_skill_gap(resume_text, st.session_state["job_desc"])
        st.text_area("Skill Gap Analysis:", skill_gap_analysis, height=300)
