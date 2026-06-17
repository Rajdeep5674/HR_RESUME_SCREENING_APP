# AI Resume Screening App 🚀

A sleek, premium, and beginner-friendly Streamlit web application that screens resume PDFs against job descriptions using:
1. **Keyword-based Matching**: A local, logic-based analyzer that compares keywords in the resume with those required by the job description.
2. **AI-powered Screening**: An advanced option using Gemini or OpenAI APIs to perform semantic screening, identifying candidate strengths, gaps, and improvements.

---

## 📂 Project Structure

```text
ai_resume_screening_app/
  │
  ├── app.py                  # Main Streamlit web application
  ├── requirements.txt        # Python libraries required
  ├── README.md               # Setup and project documentation
  ├── .env.example            # Template for environment API keys
  │
  ├── sample_resumes/         # Directory for test resumes
  └── utils/
      ├── pdf_reader.py       # Helper to extract text from PDFs
      └── resume_analyzer.py  # Algorithms for Keyword & AI screening
```

---

## 🛠️ Installation & Setup

Follow these steps to run the application on your computer:

### 1. Clone or Open the Project
Open the project directory in your terminal or editor.

### 2. Create and Activate a Virtual Environment
Using a virtual environment is highly recommended to keep dependencies isolated.

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys (Optional - for AI Mode)
If you wish to use the advanced AI-powered analyzer:
1. Create a file named `.env` in the root directory.
2. Copy the contents from `.env.example` into `.env`.
3. Add your Gemini or OpenAI API keys:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   OPENAI_API_KEY=your_actual_openai_api_key
   ```

---

## 🏃 Running the Application

Launch the Streamlit app with the following command:
```bash
streamlit run app.py
```

The app will compile and automatically open a new tab in your web browser (usually at `http://localhost:8501`).

---

## 🎓 Learning Outcomes for Students

By building or running this project, you will learn:
1. **Frontend Development with Streamlit**: How to construct inputs, display results, and implement sidebars.
2. **PDF Processing**: How to read, parse, and process text from binary PDF uploads using Python.
3. **Logic & Algorithms**: Understanding string normalisation, boundary-sensitive keyword searching, and calculating metrics.
4. **AI/LLM Integration**: Sending context prompts to Gemini or OpenAI, specifying JSON schema structures, and handling API errors gracefully.
5. **Environment Configuration**: Managing configuration values using `.env` files.
