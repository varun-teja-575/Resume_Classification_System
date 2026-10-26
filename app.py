import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import re
import os
import sys

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.append(BASE_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from parser.pdf_reader import extract_text_from_pdf
from parser.docx_reader import extract_text_from_docx
from preprocessing.clean_text import clean_resume


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background-color: #f5f7fb;
    }


    /* Header */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #6b7280;
        margin-bottom: 30px;
    }


    /* Cards */

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 14px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    .metric-title {
        font-size: 15px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
    }


    /* Prediction card */

    .prediction-card {
        background-color: white;
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0px 3px 15px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        margin-top: 20px;
    }

    .prediction-title {
        color: #6b7280;
        font-size: 16px;
    }

    .prediction-role {
        font-size: 32px;
        font-weight: 700;
        color: #111827;
    }


    /* Skill */

    .skill-box {
        display: inline-block;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 20px;
        background-color: #eef2ff;
        color: #3730a3;
        font-weight: 500;
    }


    /* Missing skill */

    .missing-box {
        display: inline-block;
        padding: 8px 14px;
        margin: 5px;
        border-radius: 20px;
        background-color: #fef2f2;
        color: #b91c1c;
        font-weight: 500;
    }


    /* Suggestion */

    .suggestion-box {
        background-color: white;
        padding: 15px 18px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #6366f1;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD ML MODEL
# ============================================================

@st.cache_resource
def load_models():

    model_path = os.path.join(
        BASE_DIR,
        "model",
        "svm_model.pkl"
    )

    tfidf_path = os.path.join(
        BASE_DIR,
        "model",
        "tfidf.pkl"
    )

    encoder_path = os.path.join(
        BASE_DIR,
        "model",
        "label_encoder.pkl"
    )

    svm_model = joblib.load(
        model_path
    )

    tfidf = joblib.load(
        tfidf_path
    )

    label_encoder = joblib.load(
        encoder_path
    )

    return (
        svm_model,
        tfidf,
        label_encoder
    )


# ============================================================
# LOAD SKILL MODULE
# ============================================================

try:

    from analyzer.skills import (
        extract_skills,
        find_missing_skills
    )

    SKILLS_MODULE_AVAILABLE = True

except Exception:

    SKILLS_MODULE_AVAILABLE = False


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📄 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Resume Classification & Intelligent Resume Analysis System'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📂 Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX"
    )

    st.markdown("---")

    st.markdown(
        """
        ### 🔍 Analysis Includes

        ✓ Job Classification

        ✓ Skill Detection

        ✓ Missing Skills

        ✓ Resume Score

        ✓ ATS Score

        ✓ Improvement Suggestions

        ✓ Analytics
        """
    )


# ============================================================
# UPLOAD AREA
# ============================================================

if uploaded_file is None:

    st.info(
        "👈 Upload a PDF or DOCX resume from the sidebar to begin analysis."
    )

    st.markdown(
        """
        <div style="
            background:white;
            padding:50px;
            border-radius:18px;
            text-align:center;
            margin-top:30px;
            border:2px dashed #d1d5db;
        ">

        <div style="font-size:60px;">📄</div>

        <h2>Upload Your Resume</h2>

        <p style="color:#6b7280;">
        Our system will analyze your resume using
        NLP and Machine Learning.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# ============================================================
# SAVE UPLOADED FILE TEMPORARILY
# ============================================================

temp_file_path = os.path.join(
    BASE_DIR,
    uploaded_file.name
)

with open(
    temp_file_path,
    "wb"
) as f:

    f.write(
        uploaded_file.getbuffer()
    )


# ============================================================
# EXTRACT TEXT
# ============================================================

with st.spinner("Reading your resume..."):

    if uploaded_file.name.lower().endswith(".pdf"):

        resume_text = extract_text_from_pdf(
            temp_file_path
        )

    else:

        resume_text = extract_text_from_docx(
            temp_file_path
        )


# ============================================================
# REMOVE TEMPORARY FILE
# ============================================================

try:

    os.remove(
        temp_file_path
    )

except Exception:

    pass


# ============================================================
# CHECK TEXT
# ============================================================

if not resume_text:

    st.error(
        "Unable to extract text from the uploaded resume."
    )

    st.stop()


st.success(
    f"Resume successfully read! "
    f"Extracted {len(resume_text)} characters."
)


# ============================================================
# PREPROCESSING
# ============================================================

with st.spinner("Preprocessing resume..."):

    cleaned_text = clean_resume(
        resume_text
    )


# ============================================================
# MACHINE LEARNING PREDICTION
# ============================================================

with st.spinner("Classifying resume..."):

    try:

        svm_model, tfidf, label_encoder = load_models()

        vectorized_text = tfidf.transform(
            [cleaned_text]
        )

        prediction = svm_model.predict(
            vectorized_text
        )

        predicted_role = label_encoder.inverse_transform(
            prediction
        )[0]


        # ----------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------

        confidence = 0

        if hasattr(
            svm_model,
            "predict_proba"
        ):

            probabilities = svm_model.predict_proba(
                vectorized_text
            )

            confidence = (
                probabilities[0].max()
                * 100
            )

        else:

            decision_scores = svm_model.decision_function(
                vectorized_text
            )

            if len(decision_scores.shape) == 1:

                confidence = 50

            else:

                exp_scores = __import__(
                    "numpy"
                ).exp(
                    decision_scores[0]
                    -
                    decision_scores[0].max()
                )

                probabilities = (
                    exp_scores
                    /
                    exp_scores.sum()
                )

                confidence = (
                    probabilities.max()
                    * 100
                )


    except Exception as e:

        st.error(
            f"Model prediction error: {e}"
        )

        st.stop()


# ============================================================
# SKILL EXTRACTION
# ============================================================

detected_skills = []


if SKILLS_MODULE_AVAILABLE:

    try:

        detected_skills = extract_skills(
            resume_text
        )

    except Exception:

        try:

            detected_skills = extract_skills(
                cleaned_text
            )

        except Exception:

            detected_skills = []


# ============================================================
# FALLBACK SKILL DICTIONARY
# ============================================================

if not detected_skills:

    skill_dictionary = [

        "python",
        "java",
        "javascript",
        "c++",
        "sql",
        "mysql",
        "mongodb",
        "html",
        "css",
        "react",
        "nodejs",
        "spring",
        "spring boot",
        "flask",
        "django",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "machine learning",
        "deep learning",
        "nlp",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "rest api"

    ]

    text_lower = resume_text.lower()

    detected_skills = [

        skill

        for skill in skill_dictionary

        if skill.lower() in text_lower

    ]


# Remove duplicates

detected_skills = list(
    dict.fromkeys(
        detected_skills
    )
)


# ============================================================
# REQUIRED SKILLS BY ROLE
# ============================================================

role_skills = {

    "Python Developer": [
        "python",
        "sql",
        "git",
        "flask",
        "django",
        "rest api",
        "docker"
    ],

    "Java Developer": [
        "java",
        "sql",
        "spring",
        "spring boot",
        "git",
        "rest api",
        "docker"
    ],

    "Data Science": [
        "python",
        "pandas",
        "numpy",
        "machine learning",
        "sql",
        "matplotlib",
        "scikit-learn"
    ],

    "Web Designing": [
        "html",
        "css",
        "javascript",
        "react"
    ],

    "DevOps Engineer": [
        "linux",
        "docker",
        "kubernetes",
        "git",
        "aws",
        "ci/cd"
    ]

}


required_skills = role_skills.get(
    predicted_role,
    []
)


missing_skills = [

    skill

    for skill in required_skills

    if skill.lower()
    not in [
        s.lower()
        for s in detected_skills
    ]

]


# ============================================================
# SKILL MATCH
# ============================================================

if required_skills:

    matched_count = (
        len(required_skills)
        -
        len(missing_skills)
    )

    skill_match = (
        matched_count
        /
        len(required_skills)
    ) * 100

else:

    skill_match = 0


# ============================================================
# CONTACT INFORMATION
# ============================================================

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

phone_pattern = (
    r'(\+?\d{1,3}[\s-]?)?'
    r'(\(?\d{3,5}\)?[\s-]?)?'
    r'\d{3,5}[\s-]?\d{4,6}'
)


email_found = re.search(
    email_pattern,
    resume_text
)

phone_found = re.search(
    phone_pattern,
    resume_text
)


if email_found and phone_found:

    contact_score = 100

elif email_found or phone_found:

    contact_score = 50

else:

    contact_score = 0


# ============================================================
# SECTION ANALYSIS
# ============================================================

sections = {

    "Education": [
        "education",
        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "degree"
    ],

    "Skills": [
        "skills",
        "technical skills",
        "technologies"
    ],

    "Projects": [
        "projects",
        "project"
    ],

    "Experience": [
        "experience",
        "work experience",
        "employment",
        "internship"
    ],

    "Certifications": [
        "certification",
        "certifications",
        "certificate"
    ],

    "Summary": [
        "summary",
        "objective",
        "profile"
    ]

}


text_lower = resume_text.lower()

section_results = {}

for section, keywords in sections.items():

    found = any(
        keyword in text_lower
        for keyword in keywords
    )

    section_results[section] = found


section_score = (
    sum(section_results.values())
    /
    len(section_results)
) * 100


# ============================================================
# RESUME LENGTH
# ============================================================

word_count = len(
    resume_text.split()
)


if word_count >= 500:

    length_score = 100

elif word_count >= 350:

    length_score = 80

elif word_count >= 200:

    length_score = 60

elif word_count >= 100:

    length_score = 40

else:

    length_score = 20


# ============================================================
# KEYWORD SCORE
# ============================================================

if required_skills:

    keyword_match = skill_match

else:

    keyword_match = min(
        len(detected_skills) * 10,
        100
    )


# ============================================================
# FORMATTING SCORE
# ============================================================

formatting_score = 100

if word_count < 200:

    formatting_score -= 30

if not email_found:

    formatting_score -= 20

if not phone_found:

    formatting_score -= 20

if not section_results["Skills"]:

    formatting_score -= 10

if not section_results["Education"]:

    formatting_score -= 10

if not section_results["Experience"]:

    formatting_score -= 10


formatting_score = max(
    0,
    formatting_score
)


# ============================================================
# ATS SCORE
# ============================================================

ats_score = (

    keyword_match * 0.40

    +

    section_score * 0.20

    +

    contact_score * 0.15

    +

    formatting_score * 0.15

    +

    length_score * 0.10

)


ats_score = round(
    ats_score,
    2
)


# ============================================================
# RESUME SCORE
# ============================================================

skills_points = min(
    len(detected_skills) * 4,
    40
)


projects_points = (
    25
    if section_results["Projects"]
    else 0
)


education_points = (
    15
    if section_results["Education"]
    else 0
)


certification_points = (
    10
    if section_results["Certifications"]
    else 0
)


experience_points = (
    10
    if section_results["Experience"]
    else 0
)


resume_score = (

    skills_points
    +
    projects_points
    +
    education_points
    +
    certification_points
    +
    experience_points

)


resume_score = min(
    resume_score,
    100
)


# ============================================================
# SUGGESTIONS
# ============================================================

suggestions = []


for skill in missing_skills[:5]:

    suggestions.append(
        f"Consider adding or learning {skill} "
        f"for the {predicted_role} role."
    )


if ats_score < 70:

    suggestions.append(
        "Improve your ATS score by adding "
        "more role-specific keywords."
    )


if not email_found:

    suggestions.append(
        "Add your email address to the resume."
    )


if not phone_found:

    suggestions.append(
        "Add your phone number to the resume."
    )


if "github" not in text_lower:

    suggestions.append(
        "Add your GitHub profile to showcase "
        "your projects and coding experience."
    )


if "linkedin" not in text_lower:

    suggestions.append(
        "Consider adding your LinkedIn profile "
        "to your resume."
    )


if not section_results["Projects"]:

    suggestions.append(
        "Add a Projects section with "
        "relevant academic or personal projects."
    )


if word_count < 250:

    suggestions.append(
        "Your resume appears too short. "
        "Add meaningful project, education and "
        "experience details."
    )


suggestions = list(
    dict.fromkeys(
        suggestions
    )
)


# ============================================================
# DASHBOARD
# ============================================================

st.markdown("---")


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        Resume Score
        </div>

        <div class="metric-value">
        {resume_score}/100
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        ATS Score
        </div>

        <div class="metric-value">
        {ats_score}/100
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        Skill Match
        </div>

        <div class="metric-value">
        {skill_match:.1f}%
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">

        <div class="metric-title">
        Skills Detected
        </div>

        <div class="metric-value">
        {len(detected_skills)}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION
# ============================================================

st.markdown(
    f"""
    <div class="prediction-card">

    <div class="prediction-title">
    Predicted Job Category
    </div>

    <div class="prediction-role">
    💼 {predicted_role}
    </div>

    <p>
    Prediction Confidence:
    <b>{confidence:.2f}%</b>
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SKILLS
# ============================================================

st.markdown("## 🛠️ Skills Analysis")


skill_col, missing_col = st.columns(2)


with skill_col:

    st.subheader(
        "✅ Detected Skills"
    )

    if detected_skills:

        html = ""

        for skill in detected_skills:

            html += (
                f'<span class="skill-box">'
                f'✓ {skill}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No predefined skills detected."
        )


with missing_col:

    st.subheader(
        "⚠️ Missing Skills"
    )

    if missing_skills:

        html = ""

        for skill in missing_skills:

            html += (
                f'<span class="missing-box">'
                f'✗ {skill}'
                f'</span>'
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "No major missing skills detected!"
        )


# ============================================================
# CHARTS
# ============================================================

st.markdown("---")

st.markdown(
    "## 📊 Resume Analytics"
)


chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    score_data = pd.DataFrame({

        "Metric": [
            "Resume Score",
            "ATS Score",
            "Skill Match"
        ],

        "Score": [
            resume_score,
            ats_score,
            skill_match
        ]

    })


    fig = px.bar(

        score_data,

        x="Metric",

        y="Score",

        range_y=[0, 100],

        text="Score",

        title="Resume Performance"

    )


    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )


    fig.update_layout(
        height=400
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


with chart_col2:

    skill_chart = pd.DataFrame({

        "Category": [
            "Detected Skills",
            "Missing Skills"
        ],

        "Count": [
            len(detected_skills),
            len(missing_skills)
        ]

    })


    fig2 = px.pie(

        skill_chart,

        names="Category",

        values="Count",

        title="Skill Distribution",

        hole=0.4

    )


    fig2.update_layout(
        height=400
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# ============================================================
# ATS DETAILS
# ============================================================

st.markdown("---")

st.markdown(
    "## 📋 ATS Analysis"
)


ats_col1, ats_col2 = st.columns(2)


with ats_col1:

    st.write(
        f"**Keyword Match:** "
        f"{keyword_match:.2f}%"
    )

    st.write(
        f"**Section Score:** "
        f"{section_score:.2f}%"
    )

    st.write(
        f"**Contact Information:** "
        f"{contact_score:.2f}%"
    )


with ats_col2:

    st.write(
        f"**Formatting Score:** "
        f"{formatting_score:.2f}%"
    )

    st.write(
        f"**Resume Length:** "
        f"{length_score:.2f}%"
    )

    st.write(
        f"**Word Count:** "
        f"{word_count}"
    )


# ============================================================
# RESUME SECTIONS
# ============================================================

st.markdown("---")

st.markdown(
    "## 📑 Resume Sections"
)


section_data = pd.DataFrame({

    "Section": list(
        section_results.keys()
    ),

    "Status": [

        "Present"
        if value
        else "Missing"

        for value
        in section_results.values()

    ]

})


st.dataframe(
    section_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# SUGGESTIONS
# ============================================================

st.markdown("---")

st.markdown(
    "## 💡 Resume Improvement Suggestions"
)


if suggestions:

    for i, suggestion in enumerate(
        suggestions,
        start=1
    ):

        st.markdown(
            f"""
            <div class="suggestion-box">

            <b>{i}.</b>
            {suggestion}

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.success(
        "🎉 Your resume looks good!"
    )


# ============================================================
# ORIGINAL RESUME TEXT
# ============================================================

with st.expander(
    "📄 View Extracted Resume Text"
):

    st.text(
        resume_text
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6b7280;
        padding:20px;
    ">

    <b>AI Resume Analyzer</b>

    <br>

    NLP + TF-IDF + Support Vector Machine

    </div>
    """,
    unsafe_allow_html=True
)