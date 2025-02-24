import streamlit as st
import google.generativeai as genai

# Configure Gemini API Key (Ensure security by using environment variables)
genai.configure(api_key="AIzaSyDJrBU_Q0hWvuw6wL_lI4EClmutjP4PW5I")

# Streamlit App Configuration
st.set_page_config(page_title="Interview Prep", layout="wide")
st.title("Interview Prep")
st.write("Practice with role-specific interview questions")

# User input for job role
job_role = st.text_input("Enter the Job Role:", "Software Engineer")

# Function to generate open-ended questions using AI
def generate_questions(job_role):
    prompt = f"""
    Generate 5 open-ended interview questions for a {job_role} interview.
    Each question should assess technical knowledge, problem-solving skills, or behavioral competencies.
    Format:
    Q1: Question text
    Q2: Question text
    ...
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip().split("\n") if response else []
    except Exception as e:
        return [f"Error generating questions: {str(e)}"]

# Generate and display questions
if st.button("Start Mock Interview"):
    with st.spinner("Generating questions..."):
        questions = generate_questions(job_role)
        
        if not questions or "Error" in questions[0]:
            st.error("⚠️ Failed to generate questions. Please try again.")
        else:
            st.session_state["questions"] = questions
            st.session_state["responses"] = {q: "" for q in questions}
            st.session_state["submitted"] = False

# Display questions and allow user input
if "questions" in st.session_state and not st.session_state.get("submitted", False):
    st.subheader(f"📌 Mock Interview for {job_role}")
    
    for idx, question in enumerate(st.session_state["questions"], start=1):
        st.session_state["responses"][question] = st.text_area(f"**Q{idx}: {question}**", 
                                                               key=f"q{idx}")

    # Submit button
    if st.button("Submit Answers"):
        st.session_state["submitted"] = True  # Mark as submitted

# Display feedback after submission
if st.session_state.get("submitted", False):
    st.subheader("🔍 Feedback & Suggestions")

    # Function to get AI feedback on responses
    def get_feedback(questions_responses):
        prompt = "Provide feedback on the following interview answers:\n\n"
        for q, ans in questions_responses.items():
            prompt += f"**Question:** {q}\n**Answer:** {ans}\n\n"
        prompt += "For each answer, highlight strengths and areas for improvement."
        
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            return response.text.strip().split("\n\n") if response else []
        except Exception as e:
            return [f"Error generating feedback: {str(e)}"]

    # Get AI-generated feedback
    feedback_list = get_feedback(st.session_state["responses"])
    
    for idx, feedback in enumerate(feedback_list):
        st.info(f"📝 **Feedback for Q{idx+1}:**\n{feedback}")

    st.success("🎯 Keep practicing to improve your responses!")

