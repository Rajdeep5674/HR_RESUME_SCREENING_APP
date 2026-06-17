# AI Resume Screening App

## Project Title

AI Resume Screening App using Python, Streamlit, PDF Processing, and AI

## Project Objective

The goal of this project is to build a simple AI-powered HR tool where a user can upload a resume PDF, paste a job description, and get an automatic resume match analysis.

This project is perfect for showcasing agentic AI because Codex can help create the full application from a single project requirement.

## Real-World Use Case

Companies receive many resumes for a single job role. Manually checking every resume takes time. This app helps HR teams quickly understand:

- How well a resume matches a job description
- Which skills are present in the resume
- Which important skills are missing
- What improvements the candidate should make

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| PDF Text Extraction | pdfplumber or PyPDF |
| AI Analysis | OpenAI API / Gemini API / rule-based matching |
| Deployment | Streamlit Cloud |
| Development Agent | Codex |

## Main Features

1. Upload resume in PDF format
2. Extract text from the uploaded resume
3. Enter or paste job description
4. Compare resume with job description
5. Show resume match percentage
6. Display matched skills
7. Display missing skills
8. Suggest resume improvement points
9. Show a clean Streamlit dashboard
10. Make the code beginner-friendly for students

## User Flow

```text
START
  |
  v
Upload Resume PDF
  |
  v
Extract Resume Text
  |
  v
Paste Job Description
  |
  v
AI / Logic Compares Resume with Job Description
  |
  v
Generate Match Percentage
  |
  v
Show Matched Skills, Missing Skills, and Suggestions
  |
  v
END
```

## Suggested Folder Structure

```text
ai_resume_screening_app/
  |
  |-- app.py
  |-- requirements.txt
  |-- README.md
  |-- sample_resumes/
  |-- utils/
      |-- pdf_reader.py
      |-- resume_analyzer.py
```

## Required Python Libraries

```text
streamlit
pdfplumber
pandas
python-dotenv
openai
```

If you want to build a simple version without paid AI API, you can use only:

```text
streamlit
pdfplumber
pandas
```

## Simple Version Logic

In the beginner-friendly version, the app can compare skills using keyword matching.

Example skill list:

```python
skills = [
    "python",
    "sql",
    "power bi",
    "excel",
    "machine learning",
    "pandas",
    "numpy",
    "communication",
    "data analysis"
]
```

The app checks which skills are present in the resume and job description.

## Match Percentage Formula

```text
Match Percentage = (Number of Matched Skills / Number of Required Skills) * 100
```

Example:

```text
Required Skills = 10
Matched Skills = 7

Match Percentage = (7 / 10) * 100 = 70%
```

## Codex Prompt

Use this prompt inside Codex:

```text
Create a Streamlit AI Resume Screening App.

Requirements:
1. User can upload a resume PDF.
2. Extract text from the uploaded PDF using pdfplumber.
3. User can paste a job description.
4. Extract important skills from the job description.
5. Compare resume text with required skills.
6. Show match percentage.
7. Show matched skills.
8. Show missing skills.
9. Suggest resume improvement points.
10. Keep the UI clean, professional, and beginner-friendly.
11. Add comments in the code so students can understand.
12. Create requirements.txt also.
```

## Advanced Codex Prompt With AI API

```text
Build a Streamlit resume screening app using Python.

Features:
1. Upload resume PDF.
2. Extract text from PDF.
3. Paste job description.
4. Use an AI model to compare resume and job description.
5. Return:
   - match percentage
   - matched skills
   - missing skills
   - candidate strengths
   - resume improvement suggestions
6. Display output in a clean dashboard.
7. Keep API key in .env file.
8. Add proper error handling.
9. Create requirements.txt and README.md.
```

## Sample App Output

```text
Resume Match Score: 82%

Matched Skills:
- Python
- SQL
- Power BI
- Excel
- Data Analysis

Missing Skills:
- Machine Learning
- Cloud Database
- Dashboard Automation

Improvement Suggestions:
- Add 2-3 data analytics projects.
- Mention SQL queries used in real projects.
- Add Power BI dashboard screenshots or links.
- Include measurable achievements.
```

## Streamlit UI Sections

The app should contain these sections:

1. App title
2. Resume upload section
3. Job description text area
4. Analyze button
5. Match score card
6. Matched skills section
7. Missing skills section
8. Improvement suggestions section

## Reel Script For Facebook

### Opening Hook

```text
Can AI screen resumes like an HR?
আজ Codex দিয়ে বানাবো AI Resume Screening App.
```

### Scene 1

Show blank folder and say:

```text
এখানে এখনও কোনো code নেই.
```

### Scene 2

Show Codex prompt:

```text
Build a Streamlit AI Resume Screening App.
```

### Scene 3

Show Codex creating files:

```text
Codex নিজে app.py, requirements.txt, আর logic তৈরি করছে.
```

### Scene 4

Run the app:

```text
এবার resume upload করলাম এবং job description দিলাম.
```

### Scene 5

Show result:

```text
AI বলছে resume match score 82%.
Matched skills, missing skills, suggestions সব দেখাচ্ছে.
```

### Closing Line

```text
AI coding replace করবে না,
কিন্তু যারা AI agent use করতে জানবে,
তারা project অনেক দ্রুত build করতে পারবে.
```

## Facebook Caption

```text
Codex দিয়ে বানালাম AI Resume Screening App 🔥

Resume upload করো,
Job description দাও,
AI বলে দেবে কত % match করছে।

Python + Streamlit + AI Agent = Real-world HR Project

যারা Python শিখছো, তাদের জন্য এটা perfect portfolio project.

Comment "RESUME" for full project roadmap.
```

## Learning Outcomes

After completing this project, students will learn:

1. How to build a Streamlit app
2. How to upload files in Streamlit
3. How to extract text from PDF
4. How to compare text data
5. How to calculate match percentage
6. How to display results in dashboard format
7. How to use Codex for project development
8. How AI agents can speed up real-world app development

## Future Enhancements

1. Add login system for HR users
2. Store uploaded resume results in MySQL
3. Add candidate ranking system
4. Upload multiple resumes at once
5. Export result as PDF report
6. Add email sending feature
7. Deploy the app on Streamlit Cloud
8. Create a Power BI dashboard from screening results

## Best Version For Students

For beginners, start with keyword-based matching.

For advanced students, add AI API-based resume analysis.

Recommended teaching order:

1. Streamlit UI
2. PDF text extraction
3. Skill keyword matching
4. Match percentage calculation
5. Dashboard display
6. AI API integration
7. Deployment

