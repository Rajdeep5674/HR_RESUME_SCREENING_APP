import streamlit as st
import os
import io
from dotenv import load_dotenv

# Import our utilities
from utils.pdf_reader import extract_text_from_pdf
from utils.resume_analyzer import analyze_resume_keywords, analyze_resume_ai

# Load environment variables from .env
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Resume Screening Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (CSS Injection for Premium Aesthetics)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    /* Apply styles */
    .stApp {
        font-family: 'Outfit', sans-serif;
        background-color: #0d0e15;
        color: #e2e8f0;
    }
    
    /* Premium Title Header */
    .header-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(99, 102, 241, 0.15);
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(5px);
        text-align: center;
    }
    
    .header-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    /* Section Headers */
    h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        color: #f8fafc !important;
        margin-top: 15px !important;
    }
    
    /* Glassmorphism Cards */
    .card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
    }
    
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #818cf8;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 8px;
    }
    
    /* Radial Match Score Layout */
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }
    
    .radial-progress {
        width: 150px;
        height: 150px;
    }
    
    .circle-bg {
        fill: none;
        stroke: #1e293b;
        stroke-width: 2.8;
    }
    
    .circle {
        fill: none;
        stroke-width: 2.8;
        stroke-linecap: round;
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }
    
    .percentage {
        fill: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 8px;
        font-weight: bold;
        text-anchor: middle;
    }
    
    /* Custom Skill Chips */
    .chip {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .chip-matched {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .chip-matched:hover {
        background: rgba(16, 185, 129, 0.25);
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
    }
    
    .chip-missing {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .chip-missing:hover {
        background: rgba(245, 158, 11, 0.25);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.2);
    }
    
    /* Dynamic Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Sidebar styling */
    .css-1d391tw, [data-testid="stSidebar"] {
        background-color: #090a0f !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sample Data Definitions (For Instant Demos)
# ---------------------------------------------------------
SAMPLE_JD = """We are looking for a Senior Python Developer to join our team. 
The ideal candidate will have strong experience with Python, SQL, and Git. 
Experience with building APIs using FastAPI or Flask, and containerization using Docker is required.
Knowledge of cloud databases (AWS or GCP), Pandas, and Machine Learning models is a plus. 
Strong Communication skills and Agile/Scrum experience are required."""

SAMPLE_RESUME = """Jane Doe - Software Engineer
Email: jane.doe@example.com | GitHub: github.com/janedoe

Summary:
Passionate Software Engineer with 4 years of experience building scalable web applications and data pipelines. 
Experienced in Python, SQL, and Git version control. Great communication skills and used to agile environments.

Skills:
- Languages: Python, SQL, JavaScript, HTML, CSS
- Frameworks: FastAPI, Flask, Pandas, NumPy
- Databases: PostgreSQL, MongoDB, MySQL
- Developer Tools: Git, Docker, Jira
- Soft Skills: Communication, Teamwork, Problem Solving, Agile, Scrum

Experience:
Software Engineer | Tech Corp (2022 - Present)
- Developed and maintained RESTful APIs using Python and FastAPI.
- Collaborated with team members using Agile/Scrum methodologies.
- Managed containerized services with Docker and deployed to test environments.
- Utilized Pandas for basic data analysis and reporting.
"""

# Initialize session states
if "jd_text" not in st.session_state:
    st.session_state["jd_text"] = ""
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""
if "resume_name" not in st.session_state:
    st.session_state["resume_name"] = ""

# ---------------------------------------------------------
# Sidebar Component (Settings Panel)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/resume.png", width=64)
    st.markdown("## Configuration Settings")
    st.markdown("Customize your screen analysis engine here.")
    
    # Mode switch
    mode = st.radio(
        "Screening Mode",
        options=["Keyword Match (Beginner)", "AI-powered (Advanced)"],
        index=0,
        help="Keyword Match works locally without API keys. AI mode uses a Large Language Model for deep semantic screening."
    )
    
    # AI Engine Settings
    ai_provider = None
    api_key = None
    if mode == "AI-powered (Advanced)":
        st.markdown("---")
        st.markdown("### AI API Settings")
        ai_provider = st.selectbox("Select AI Provider", options=["Gemini", "OpenAI"])
        
        # Look for default env key
        env_key = ""
        if ai_provider == "Gemini":
            env_key = os.getenv("GEMINI_API_KEY", "")
            key_label = "Gemini API Key"
            key_help = "Get a key from Google AI Studio"
        else:
            env_key = os.getenv("OPENAI_API_KEY", "")
            key_label = "OpenAI API Key"
            key_help = "Get a key from OpenAI Platform Dashboard"
            
        if env_key:
            st.success(f"🔑 API Key detected in `.env` file")
            api_key = st.text_input(key_label, value=env_key, type="password", help=key_help)
        else:
            st.warning("⚠️ No API Key found in `.env`. Paste one below:")
            api_key = st.text_input(key_label, placeholder="Paste your API key here...", type="password", help=key_help)
            
    st.markdown("---")
    st.markdown("### Interactive Sandbox")
    st.markdown("Click below to auto-populate sample data and test the application instantly.")
    
    if st.button("🚀 Load Sample Data", use_container_width=True):
        st.session_state["jd_text"] = SAMPLE_JD
        st.session_state["resume_text"] = SAMPLE_RESUME
        st.session_state["resume_name"] = "sample_developer_resume.txt"
        st.rerun()

# ---------------------------------------------------------
# Header & Dashboard Intro
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">📄 AI Resume Screening Hub</div>
    <div class="header-subtitle">Analyze, parse and optimize resume matches against job profiles instantly</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Input Section
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">1. Upload Resume</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Candidate Resume (PDF format)",
        type=["pdf"],
        help="Please upload a PDF document containing the resume text."
    )
    
    if uploaded_file is not None:
        try:
            # Check if it's a new upload or matches session state
            if st.session_state["resume_name"] != uploaded_file.name:
                with st.spinner("Extracting text from PDF..."):
                    extracted = extract_text_from_pdf(uploaded_file)
                    st.session_state["resume_text"] = extracted
                    st.session_state["resume_name"] = uploaded_file.name
                st.success("✅ PDF text successfully parsed!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            
    # Display preview or status
    if st.session_state["resume_text"]:
        st.markdown(f"**Active Resume File:** `{st.session_state['resume_name'] or 'Loaded via Demo'}`")
        with st.expander("👁️ Preview Extracted Resume Text"):
            st.text_area(
                "Extracted Text content", 
                value=st.session_state["resume_text"], 
                height=200, 
                disabled=True,
                label_visibility="collapsed"
            )
    else:
        st.info("ℹ️ Upload a resume PDF or load sample data from the sidebar to begin.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">2. Job Description</div>', unsafe_allow_html=True)
    
    jd_input = st.text_area(
        "Paste the Job Description requirements here:",
        value=st.session_state["jd_text"],
        placeholder="We are looking for a software engineer with Python...",
        height=240,
        help="Enter details about the job role, required skills, and qualifications."
    )
    st.session_state["jd_text"] = jd_input
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Trigger Action Button
# ---------------------------------------------------------
st.markdown("<div style='text-align: center; margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)
analyze_btn = st.button("🔍 Match and Screen Candidate", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Analysis and Results Dashboard
# ---------------------------------------------------------
if analyze_btn:
    # Validation
    if not st.session_state["resume_text"]:
        st.error("❌ Please upload a resume PDF or click 'Load Sample Data' in the sidebar first.")
    elif not st.session_state["jd_text"]:
        st.error("❌ Please provide a Job Description to match the resume against.")
    else:
        # Proceed with Analysis
        with st.spinner("Screening candidate against job specifications..."):
            try:
                results = None
                if mode == "Keyword Match (Beginner)":
                    results = analyze_resume_keywords(
                        st.session_state["resume_text"],
                        st.session_state["jd_text"]
                    )
                else:
                    # AI-powered
                    if not api_key:
                        st.error(f"❌ API Key is required for AI Mode. Please configure a key in the sidebar or `.env` file.")
                    else:
                        results = analyze_resume_ai(
                            st.session_state["resume_text"],
                            st.session_state["jd_text"],
                            ai_provider,
                            api_key
                        )
                
                if results:
                    st.markdown("## 📊 Screening Results & Candidate Report")
                    
                    # Dashboard Layout
                    res_col1, res_col2 = st.columns([1, 2], gap="medium")
                    
                    with res_col1:
                        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
                        st.markdown('<div class="card-title" style="text-align: center;">Match Score</div>', unsafe_allow_html=True)
                        
                        score = results["match_percentage"]
                        
                        # Set color based on score value
                        if score >= 75:
                            stroke_color = "#10b981"  # green
                        elif score >= 50:
                            stroke_color = "#f59e0b"  # yellow/orange
                        else:
                            stroke_color = "#ef4444"  # red
                            
                        # Custom SVG radial gauge implementation
                        st.markdown(f"""
                        <div class="score-container">
                            <svg class="radial-progress" viewBox="0 0 36 36">
                                <defs>
                                    <linearGradient id="score-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                                        <stop offset="0%" stop-color="{stroke_color}" />
                                        <stop offset="100%" stop-color="#4338ca" />
                                    </linearGradient>
                                </defs>
                                <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                                <path class="circle" stroke="url(#score-grad)" stroke-dasharray="{score}, 100" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                                <text x="18" y="20.35" class="percentage">{score}%</text>
                            </svg>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Match status label
                        if score >= 75:
                            st.markdown("<h4 style='color: #34d399; text-align: center;'>Strong Fit</h4>", unsafe_allow_html=True)
                        elif score >= 50:
                            st.markdown("<h4 style='color: #fbbf24; text-align: center;'>Potential Fit</h4>", unsafe_allow_html=True)
                        else:
                            st.markdown("<h4 style='color: #f87171; text-align: center;'>Needs Improvement</h4>", unsafe_allow_html=True)
                            
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    with res_col2:
                        st.markdown('<div class="card" style="height: 100%;">', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">Skills Assessment</div>', unsafe_allow_html=True)
                        
                        # Matched Skills
                        st.markdown("##### ✅ Matched Skills:")
                        matched = results.get("matched_skills", [])
                        if matched:
                            chips_html = "".join([f'<span class="chip chip-matched">{s}</span>' for s in matched])
                            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)
                        else:
                            st.write("No matching skills identified.")
                            
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Missing Skills
                        st.markdown("##### ❌ Missing Core Skills / Requirements:")
                        missing = results.get("missing_skills", [])
                        if missing:
                            chips_html = "".join([f'<span class="chip chip-missing">{s}</span>' for s in missing])
                            st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)
                        else:
                            st.success("No missing skills identified! Candidate matches all specified keywords.")
                            
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    # Second row of dashboard
                    st.markdown("<br>", unsafe_allow_html=True)
                    insights_col1, insights_col2 = st.columns([1, 1], gap="medium")
                    
                    with insights_col1:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">🌟 Key Strengths</div>', unsafe_allow_html=True)
                        strengths = results.get("strengths", [])
                        if strengths:
                            for s in strengths:
                                st.markdown(f"🔹 {s}")
                        else:
                            st.write("Candidate shows standard background matching.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    with insights_col2:
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        st.markdown('<div class="card-title">💡 Actionable Suggestions for Candidate</div>', unsafe_allow_html=True)
                        suggestions = results.get("suggestions", [])
                        if suggestions:
                            for sug in suggestions:
                                st.markdown(f"💡 {sug}")
                        else:
                            st.write("No major suggestions needed; resume is highly aligned.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"An error occurred during screening: {e}")
