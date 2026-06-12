# Recruitment Assistant

This is a simple tool built with Streamlit, LangChain, and Groq that makes it easy to screen resumes and prepare for interviews. It reviews a candidate's resume, grades how well it fits a specific job, and points out exactly what is missing—all without saving any personal information or files.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app

---

## Who is this for?

* **Recruiters & Hiring Managers:** Instead of reading every line of a huge stack of PDFs, you can upload a resume and instantly see a match score. The app shows you exactly which skills the candidate has and where they fall short. It also gives you a list of custom interview questions based on their skill gaps so you are ready for a screening call in seconds.
* **Job Seekers:** You can check why your resume isn't getting past automatic filters. By selecting a target role or pasting a specific job description, you can see exactly which keywords the app catches and which ones it misses, helping you fix your resume before you apply.

---

## What the App Does

1. **Resume Screening Report:** Calculates an overall profile match percentage layout. It uses smart vector similarity lookups instead of basic keyword tracking, meaning it understands related skills even if you didn't use the exact matching word.
2. **Document Verification Q&A:** A clean search sandbox where you can ask direct questions about the document data, like *"How many years of experience does this person have with React?"* or *"What did they do at their last company?"*
3. **Interview Questions:** Generates localized assessment questions tailored specifically to the candidate's core profile gaps. You can tune the output complexity tiers (Easy, Medium, Hard) and select the specific evaluation domain (Technical, Behavioral, or Situational).
4. **Refinement Suggestions:** Delivers an actionable blueprint on how to restructure or polish target blocks of your document (such as your Professional Summary, Work Experience, or Projects layout) to better align with target requirements.

---

## How the App Works

When you upload a PDF resume, the app uses a python package (`PyPDF2`) to extract all the raw text. It then breaks that text down into small, overlapping chunks and creates a mini digital map of the sentences using word context (these are called vector embeddings). This map is stored temporarily in your computer's short-term memory using a lightweight vector lookup database called FAISS.

Depending on what you select in the settings panel, matching happens in one of two ways:

1. **Using a Pre-set Role:** If you choose a standard job title from the menu (like *Data Scientist*), the app takes our built-in list of key industry skills for that job and searches your resume's digital map. It looks for matching skills based on how close the concepts are—not just exact words.
2. **Using a Custom Job Description:** If you paste a custom job description into the text box *after* selecting a role, the app skips the built-in list. It passes the pasted job text to an AI model (`Llama 3.3 70B` via Groq), extracts the most important skills from that specific text, and runs a fresh similarity search against your resume using those custom keywords.

Once the search is done, the app calculates your final score, highlights which keywords were found or missed, and uses the AI model to generate custom interview questions and tips to fix your resume based on your exact skill gaps.

---

## Quick Setup for Developers

### 1. Download and Install
Open your terminal and run these commands to clone the code and install the required packages:

```bash
git clone [https://github.com/nitinraj1234/Recruitment-Assistant.git](https://github.com/nitinraj1234/Recruitment-Assistant.git)
cd Recruitment-Assistant
pip install -r requirements.txt
