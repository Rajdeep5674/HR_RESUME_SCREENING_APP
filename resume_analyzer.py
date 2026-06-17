import re
import json
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A comprehensive list of common skills across various domains
COMMON_SKILLS = [
    # Programming Languages
    "Python", "SQL", "Java", "C++", "C#", "JavaScript", "TypeScript", "Ruby", "PHP", "Go", "Rust", "Kotlin", "Swift", "R", "Scala", "HTML", "CSS",
    # Web & Software Dev
    "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", "Laravel", "Tailwind CSS", "Bootstrap",
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub", "CI/CD", "Jenkins", "Terraform", "Ansible", "Linux", "Unix",
    # Data & Analytics
    "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Keras", "Spark", "Hadoop", "Tableau", "Power BI", "Excel", "Data Analysis", "Data Science", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Statistics", "Data Engineering", "Big Data",
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQL Server", "SQLite", "Cassandra",
    # Management & Soft Skills
    "Project Management", "Agile", "Scrum", "Jira", "Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management", "Critical Thinking", "Negotiation", "Collaboration",
    # Other business domains
    "Marketing", "SEO", "Sales", "Finance", "Accounting", "Product Management", "UI/UX", "Graphic Design", "Cybersecurity", "Networking"
]

def find_skill_in_text(text: str, skill: str) -> bool:
    """
    Search for a skill in a text with custom word boundaries to handle
    characters like C++, C#, .NET, etc.
    """
    text_lower = text.lower()
    skill_lower = skill.lower()
    
    if skill_lower not in text_lower:
        return False
        
    idx = 0
    while True:
        idx = text_lower.find(skill_lower, idx)
        if idx == -1:
            return False
            
        # Check character before
        start_ok = True
        if idx > 0:
            char_before = text_lower[idx - 1]
            # If char before is letter or number, it's not a word boundary
            if char_before.isalnum():
                start_ok = False
                
        # Check character after
        end_ok = True
        end_idx = idx + len(skill_lower)
        if end_idx < len(text_lower):
            char_after = text_lower[end_idx]
            # Avoid matching "c" in "c++" or "c#"
            if char_after.isalnum() or char_after in ['+', '#']:
                end_ok = False
                
        if start_ok and end_ok:
            return True
            
        idx += 1

def analyze_resume_keywords(resume_text: str, job_description: str) -> dict:
    """
    Beginner-friendly analysis using keyword matching.
    Calculates match percentage based on the intersection of skills
    found in both the job description and the resume.
    """
    # Find required skills from the job description
    required_skills = []
    for skill in COMMON_SKILLS:
        if find_skill_in_text(job_description, skill):
            required_skills.append(skill)
            
    # If no common skills detected in Job Description, fall back to matching
    # any skill from the list that is present in the resume.
    if not required_skills:
        # User might have written custom skills, or JD is short.
        # We will assume a default list of skills or search for any skills.
        # For evaluation, let's treat any skills mentioned in JD as required.
        # If JD is completely empty of common skills, let's suggest some.
        pass

    matched_skills = []
    missing_skills = []
    
    for skill in required_skills:
        if find_skill_in_text(resume_text, skill):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # Calculate score
    if required_skills:
        match_percentage = int((len(matched_skills) / len(required_skills)) * 100)
    else:
        # Fallback: check if resume contains any skills at all
        resume_present_skills = [s for s in COMMON_SKILLS if find_skill_in_text(resume_text, s)]
        if resume_present_skills:
            match_percentage = 50  # default moderate match if JD is generic
            matched_skills = resume_present_skills[:5]
            missing_skills = ["No specific required skills found in job description. Update JD to get missing skills."]
        else:
            match_percentage = 0
            missing_skills = ["No skills detected in resume. Add keywords relevant to the job."]

    # Generate suggestions based on missing skills and overall score
    suggestions = []
    for skill in missing_skills[:4]:
        if "Update JD" not in skill and "No skills" not in skill:
            suggestions.append(f"Add projects or experience demonstrating your proficiency in '{skill}'.")
            suggestions.append(f"List '{skill}' explicitly under your skills section if you have experience with it.")
            
    # Standard improvements
    suggestions.append("Quantify your professional achievements (e.g., 'improved efficiency by 20%').")
    suggestions.append("Tailor your summary section to directly align with the job description.")
    
    # Strengths
    strengths = []
    if matched_skills:
        strengths.append(f"Strong foundation in core skills: {', '.join(matched_skills[:3])}.")
    if match_percentage >= 70:
        strengths.append("High alignment with the core requirements of this role.")
    else:
        strengths.append("Possesses basic transferrable skills, but needs key alignment on missing technologies.")

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "suggestions": list(set(suggestions))[:5] # Limit to 5 suggestions
    }

def analyze_resume_ai(resume_text: str, job_description: str, provider: str, api_key: str) -> dict:
    """
    Advanced analysis using AI API (Gemini or OpenAI).
    Sends resume and job description to the model and requests structured JSON output.
    """
    prompt = f"""
You are an expert HR Screening Assistant and ATS (Applicant Tracking System) optimizer.
Compare the candidate's Resume Text against the Job Description.

Analyze the following:
1. Match score (0 to 100) based on alignment of experience, skills, and qualifications.
2. Skills present in the resume that match the job description.
3. Important skills/requirements from the job description that are missing in the resume.
4. Top candidate strengths for this role.
5. Actionable resume improvement suggestions to better align with the job.

Resume Text:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"

You MUST output ONLY a valid JSON object. Do not include markdown code block formatting (like ```json).
The JSON object must strictly match this schema:
{{
    "match_percentage": <int, 0 to 100>,
    "matched_skills": [<string>, ...],
    "missing_skills": [<string>, ...],
    "strengths": [<string>, ...],
    "suggestions": [<string>, ...]
}}
"""

    if provider.lower() == "gemini":
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for fast, low-cost text analysis
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        result_text = response.text.strip()
        
    elif provider.lower() == "openai":
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional ATS scanner that outputs strictly JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        result_text = response.choices[0].message.content.strip()
        
    else:
        raise ValueError(f"Unsupported AI Provider: {provider}")

    # Parse JSON
    try:
        # Strip potential markdown formatting if model didn't obey
        if result_text.startswith("```"):
            # Remove leading/trailing lines
            lines = result_text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            result_text = "\n".join(lines).strip()
            
        data = json.loads(result_text)
        
        # Ensure all required keys are present with proper types
        data["match_percentage"] = int(data.get("match_percentage", 0))
        data["matched_skills"] = list(data.get("matched_skills", []))
        data["missing_skills"] = list(data.get("missing_skills", []))
        data["strengths"] = list(data.get("strengths", []))
        data["suggestions"] = list(data.get("suggestions", []))
        
        return data
    except Exception as e:
        logger.error(f"Error parsing AI response: {str(e)}. Response text: {result_text}")
        raise RuntimeError("Failed to parse the AI analysis result. Please retry.")
