import os
import gradio as gr
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_resume(name, email, phone, job_role, experience, skills, education, achievements):

    system_prompt = """You are a professional resume writer with 10+ years of experience. 
    Given the user's details, generate a clean, ATS-friendly resume in plain text format.
    Structure it with these sections:
    - CONTACT INFORMATION
    - PROFESSIONAL SUMMARY (2-3 lines)
    - SKILLS
    - WORK EXPERIENCE
    - EDUCATION
    - ACHIEVEMENTS
    Be concise, professional, and impactful."""

    user_prompt = f"""
    Create a professional resume for:
    Name: {name}
    Email: {email}
    Phone: {phone}
    Target Job Role: {job_role}
    Years of Experience: {experience}
    Skills: {skills}
    Education: {education}
    Achievements: {achievements}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


def generate_cover_letter(name, job_role, company_name, job_description, resume_text):

    system_prompt = """You are an expert career coach and professional writer.
    Given the candidate's resume and a job description, write a compelling, 
    personalized cover letter. 
    - Keep it under 300 words
    - Use a professional but warm tone
    - Highlight how the candidate's skills match the job
    - End with a strong call to action"""

    user_prompt = f"""
    Write a cover letter for:
    Candidate Name: {name}
    Applying For: {job_role}
    Company Name: {company_name}
    
    Job Description:
    {job_description}
    
    Candidate's Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


def generate_both(name, email, phone, job_role, experience,
                  skills, education, achievements, company_name, job_description):
    try:
        resume = generate_resume(name, email, phone, job_role,
                                 experience, skills, education, achievements)
        cover_letter = generate_cover_letter(name, job_role,
                                             company_name, job_description, resume)
        return resume, cover_letter
    except Exception as e:
        error_msg = f"❌ ERROR: {str(e)}"
        return error_msg, error_msg


with gr.Blocks(title="AI Resume & Cover Letter Generator") as app:

    gr.Markdown("# 📄 AI Resume & Cover Letter Generator")
    gr.Markdown("Fill in your details below and let AI craft your professional resume and cover letter!")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 👤 Personal Details")
            name       = gr.Textbox(label="Full Name", placeholder="e.g. Rahul Sharma")
            email      = gr.Textbox(label="Email", placeholder="rahul@email.com")
            phone      = gr.Textbox(label="Phone Number", placeholder="+91 9876543210")
            job_role   = gr.Textbox(label="Target Job Role", placeholder="e.g. AI Engineer")
            experience = gr.Textbox(label="Years of Experience", placeholder="e.g. 0")

        with gr.Column():
            gr.Markdown("### 📋 Professional Details")
            skills       = gr.Textbox(label="Skills", placeholder="Python, SQL, JavaScript", lines=2)
            education    = gr.Textbox(label="Education", placeholder="B.Tech Data Science - ADYPU, 2026", lines=2)
            achievements = gr.Textbox(label="Achievements / Projects", placeholder="Built a chatbot...", lines=3)

    gr.Markdown("### 🏢 Job Details (for Cover Letter)")
    with gr.Row():
        company_name    = gr.Textbox(label="Company Name", placeholder="e.g. Google")
        job_description = gr.Textbox(label="Job Description (paste here)", lines=4,
                                      placeholder="We are looking for an AI Engineer who...")

    generate_btn = gr.Button("✨ Generate Resume & Cover Letter", variant="primary")

    gr.Markdown("---")
    gr.Markdown("## 📄 Generated Resume")
    resume_output = gr.Textbox(label="Your Resume", lines=20)

    gr.Markdown("## ✉️ Generated Cover Letter")
    cover_output  = gr.Textbox(label="Your Cover Letter", lines=15)

    generate_btn.click(
        fn=generate_both,
        inputs=[name, email, phone, job_role, experience,
                skills, education, achievements, company_name, job_description],
        outputs=[resume_output, cover_output]
    )

app.launch()