# Recruitment Assistant

This is a simple tool built with Streamlit, LangChain, and Groq that makes it easy to screen resumes and prepare for interviews. It reviews a candidate's resume, grades how well it fits a specific job, and points out exactly what is missing—all without saving any personal information or files.

Live demo: https://recruitment-assistant-bauel4dzgwouw2klwyssxj.streamlit.app

---

## Who is this for?

* **Recruiters & Hiring Managers:** Instead of reading every line of a huge stack of PDFs, you can upload a resume and instantly see a match score. The app shows you exactly which skills the candidate has and where they fall short. It also gives you a list of custom interview questions based on their skill gaps so you are ready for a screening call in seconds.
* **Job Seekers:** You can check why your resume isn't getting past automatic filters. By selecting a target role or pasting a specific job description, you can see exactly which keywords the app catches and which ones it misses, helping you fix your resume before you apply.

---

## What the App Does

1. **Smart Resume Scoring:** Calculates a match percentage. It uses smart vector search instead of basic keyword matching, meaning it understands related skills even if you didn't use the exact word.
2. **Resume Tooltips & Improvement Guide:** Gives you a clear checklist on how to fix sections of your resume (like your Experience or Projects) to better line up with the job requirements.
3. **Custom Interview Questions:** Generates interview questions tailored to the candidate's specific profile gaps. You can choose the difficulty level (Easy, Medium, Hard) and the type of question (Technical, Behavioral, or Situational).
4. **Document Chatbot:** A simple search box where you can ask direct questions about the resume, like *"How many years of experience does this person have with React?"* or *"What did they do at their last company?"*

---

## How the Scoring Changes with Custom Job Descriptions

The app handles matching in two different ways depending on what you select:

* **Using a Pre-set Role:** If you pick a role from the dropdown menu (like *AI Engineer* or *Backend Engineer*), the app scores the resume against a built-in list of industry-standard keywords.
* **Using a Custom Job Description (JD):** You can also paste text into the **"Job Specification Document"** box *after* selecting a role. When you do this, the app ignores the standard role list. Instead, it runs an AI model (Llama 3.3) to read through the pasted text, automatically extracts the most important keywords from that specific JD, and runs a brand-new similarity search against the resume.

---

## Quick Setup for Developers

### 1. Download and Install
Open your terminal and run these commands to clone the code and install the required packages:

```bash
git clone [https://github.com/nitinraj1234/Recruitment-Assistant.git](https://github.com/nitinraj1234/Recruitment-Assistant.git)
cd Recruitment-Assistant
pip install -r requirements.txt
