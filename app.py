
import os
import streamlit as st
from dotenv import load_dotenv
from agents import ResumeAnalysisAgent, ROLE_KEYWORDS

load_dotenv()

st.set_page_config(page_title="Recruitment Assistant", layout="wide")

st.sidebar.header("Configuration Settings")
api_key = os.getenv("GROQ_API_KEY", "")
cut_off = st.sidebar.slider("Minimum Screening Threshold", min_value=50, max_value=90, value=70, step=5)

st.title("Smart Recruitment Assistant")
st.subheader("Built for recruiters to screen talent, and candidates to ace the interview")

tab1, tab2, tab3, tab4 = st.tabs([
    "Resume Screening Report", 
    "Document Verification Q&A",
    "Interview Questions", 
    "Refinement Suggestions"
])

if api_key:
    if 'agent' not in st.session_state or st.session_state.get('last_key') != api_key:
        st.session_state.agent = ResumeAnalysisAgent(api_key=api_key, cut_off_score=cut_off)
        st.session_state.last_key = api_key
else:
    st.info("Provide a valid credentials key in the configuration panel to unlock evaluation functions.")

st.write("---")
st.header("Document Input Settings")

role_options = list(ROLE_KEYWORDS.keys())
selected_role = st.selectbox("Target Position Classification", options=role_options)

custom_jd = st.text_area("Job Specification Document (Optional)", placeholder="Paste target requirements definition here...")

uploaded_file = st.file_uploader("Candidate Profile Document (PDF, TXT)", type=["pdf", "txt", "PDF", "TXT"])

if uploaded_file and 'agent' in st.session_state:
    with st.spinner("Processing documents..."):
        text_content = st.session_state.agent.extract_text_from_file(uploaded_file)
        if text_content and not text_content.startswith("Error"):
            st.session_state.agent.resume_text = text_content
            st.session_state.agent.vector_store = st.session_state.agent.create_vector_store_for_pdf(text_content)
            st.success("Documents processed successfully")
        else:
            st.error(f"Processing error: {text_content}")


with tab1:
    st.header("Evaluation Analytics Summary")
    if st.button("Run Profile Analysis", key="run_analysis"):
        if 'agent' in st.session_state and st.session_state.agent.resume_text:
            with st.spinner("Analyzing resume ..."):
                res = st.session_state.agent.analyse_resume(selected_role, custom_jd if custom_jd else None)
                if "error" not in res:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Profile Score / 100", f"{res['total_score']}%")
                        if res['selected']:
                            st.success(res['reasoning'])
                        else:
                            st.error(res['reasoning'])
                    with col2:
                        st.subheader("")
                        st.write(f"**Verification Methodology:** {res['analysis_type']}")
                    st.write("### Requirement Mismatches")
                    st.write(res["weakness_details"])
                else:
                    st.error(res["error"])
        else:
            st.warning("No resume found. Please upload a file to begin")


with tab2:
    st.header("Profile Validation Terminal")
    user_query = st.text_input("Enter evaluation question:", placeholder="e.g., What is the candidate's name? List all listed projects.")
    
    if st.button("Submit Query", key="submit_qa"):
        if 'agent' in st.session_state and st.session_state.agent.resume_text:
            if user_query.strip():
                with st.spinner("Analyzing document for answer..."):
                    qa_response = st.session_state.agent.ask_question(user_query)
                    st.write("### Evaluation Output:")
                    st.write(qa_response)
            else:
                st.warning("Please enter a valid query text.")
        else:
            st.warning("No resume found. Please upload a file to begin")



with tab3:
    st.header("Assessment Questions Generator Terminal")
    q_type = st.selectbox("Domain", ["Technical", "Behavioral", "Situational"])
    diff = st.selectbox("Complexity Level", ["Easy", "Medium", "Hard"])
    count = st.slider("Question Count", 3, 10, 5)
    
    if st.button("Build Assessment Questions"):
        if 'agent' in st.session_state and st.session_state.agent.resume_text:
            with st.spinner("Generating questions..."):
                questions = st.session_state.agent.generate_interview_questions(selected_role, q_type, diff, count)
                st.markdown(questions)
        else:
            st.warning("No resume found. Please upload a file to begin")



with tab4:
    st.header("Profile Content Refinement Terminal")
    target_section = st.selectbox("Domain", ["Professional Summary", "Work Experience", "Projects", "Skills Layout"])
    if st.button("Generate Refinement "):
        if 'agent' in st.session_state and st.session_state.agent.resume_text:
            with st.spinner("Finding skills gaps..."):
                plan = st.session_state.agent.improve_resume(target_section, selected_role)
                st.markdown(plan)
        else:
            st.warning("No resume found. Please upload a file to begin")




st.markdown(
    """
    <img src="https://www.hitwebcounter.com/counter/counter.php?page=21503711&style=0005&nbdigits=5&type=ip" 
         style="display:none; width:0px; height:0px; border:0;">
    """, 
    unsafe_allow_html=True
)
