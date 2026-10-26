import re


# ============================================================
# ATS SECTION KEYWORDS
# ============================================================

SECTION_KEYWORDS = {
    "education": [
        "education",
        "academic",
        "qualification",
        "degree"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical knowledge"
    ],

    "projects": [
        "projects",
        "project",
        "academic project"
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate"
    ],

    "summary": [
        "summary",
        "objective",
        "profile",
        "professional summary"
    ]
}


# ============================================================
# IMPORTANT RESUME KEYWORDS
# ============================================================

ATS_KEYWORDS = [

    "python",
    "java",
    "javascript",
    "c++",
    "c#",
    "sql",
    "mysql",
    "mongodb",
    "html",
    "css",
    "react",
    "angular",
    "nodejs",
    "django",
    "flask",
    "spring",
    "spring boot",
    "machine learning",
    "deep learning",
    "data science",
    "numpy",
    "pandas",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "kubernetes",
    "rest api",
    "api",
    "linux",
    "agile",
    "scrum",
    "jira"
]


# ============================================================
# CONTACT INFORMATION
# ============================================================

def check_contact_information(text):

    text = text.lower()

    email_pattern = (
        r"[a-zA-Z0-9._%+-]+@"
        r"[a-zA-Z0-9.-]+\."
        r"[a-zA-Z]{2,}"
    )

    phone_pattern = (
        r"(?:\+91[\s-]?)?"
        r"[6-9]\d{9}"
    )

    email_found = bool(
        re.search(
            email_pattern,
            text
        )
    )

    phone_found = bool(
        re.search(
            phone_pattern,
            text
        )
    )

    if email_found and phone_found:

        return 100

    elif email_found or phone_found:

        return 60

    return 0


# ============================================================
# SECTION SCORE
# ============================================================

def calculate_section_score(text):

    text = text.lower()

    total_sections = len(
        SECTION_KEYWORDS
    )

    found_sections = []

    for section, keywords in SECTION_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                found_sections.append(
                    section
                )

                break

    found_sections = list(
        set(found_sections)
    )

    score = (
        len(found_sections)
        / total_sections
    ) * 100

    return round(score, 2), found_sections


# ============================================================
# KEYWORD SCORE
# ============================================================

def calculate_keyword_score(text):

    text = text.lower()

    found_keywords = []

    for keyword in ATS_KEYWORDS:

        pattern = (
            r"(?<!\w)"
            + re.escape(keyword)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text
        ):

            found_keywords.append(
                keyword
            )

    total_keywords = len(
        ATS_KEYWORDS
    )

    if total_keywords == 0:

        return 0, []

    score = (
        len(found_keywords)
        / total_keywords
    ) * 100

    return round(
        score,
        2
    ), found_keywords


# ============================================================
# RESUME LENGTH SCORE
# ============================================================

def calculate_length_score(text):

    words = text.split()

    word_count = len(words)

    # Good resume length
    if word_count >= 300:

        return 100

    elif word_count >= 200:

        return 90

    elif word_count >= 100:

        return 75

    elif word_count >= 50:

        return 50

    else:

        return 25


# ============================================================
# FORMATTING SCORE
# ============================================================

def calculate_formatting_score(text):

    score = 0

    # Email
    if re.search(
        r"[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    ):

        score += 25


    # Phone
    if re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    ):

        score += 25


    # Sections
    _, sections = (
        calculate_section_score(text)
    )


    if "skills" in sections:

        score += 10

    if "education" in sections:

        score += 10

    if "experience" in sections:

        score += 10

    if "projects" in sections:

        score += 10

    if "certifications" in sections:

        score += 10


    return min(
        score,
        100
    )


# ============================================================
# COMPLETE ATS SCORE
# ============================================================

def calculate_ats_score(text):

    if not text:

        return {
            "keyword_score": 0,
            "section_score": 0,
            "contact_score": 0,
            "formatting_score": 0,
            "length_score": 0,
            "ats_score": 0,
            "keywords": [],
            "sections": []
        }


    # Keyword score
    keyword_score, found_keywords = (
        calculate_keyword_score(text)
    )


    # Section score
    section_score, found_sections = (
        calculate_section_score(text)
    )


    # Contact score
    contact_score = (
        check_contact_information(text)
    )


    # Formatting score
    formatting_score = (
        calculate_formatting_score(text)
    )


    # Length score
    length_score = (
        calculate_length_score(text)
    )


    # ========================================================
    # FINAL WEIGHTED SCORE
    # ========================================================

    ats_score = (

        keyword_score * 0.30

        + section_score * 0.20

        + contact_score * 0.15

        + formatting_score * 0.20

        + length_score * 0.15

    )


    ats_score = round(
        ats_score,
        2
    )


    return {

        "keyword_score":
            keyword_score,

        "section_score":
            section_score,

        "contact_score":
            contact_score,

        "formatting_score":
            formatting_score,

        "length_score":
            length_score,

        "ats_score":
            ats_score,

        "keywords":
            found_keywords,

        "sections":
            found_sections
    }


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ATS SCORE ANALYZER")
    print("=" * 70)


    print(
        "\nEnter resume text."
    )

    print(
        "Type END when finished.\n"
    )


    resume_lines = []


    while True:

        line = input()

        if line.strip().upper() == "END":

            break

        resume_lines.append(
            line
        )


    resume_text = "\n".join(
        resume_lines
    )


    result = calculate_ats_score(
        resume_text
    )


    print("\n" + "=" * 70)
    print("ATS ANALYSIS")
    print("=" * 70)


    print(
        f"\nKeyword Match       : "
        f"{result['keyword_score']:.2f}%"
    )

    print(
        f"Section Score       : "
        f"{result['section_score']:.2f}%"
    )

    print(
        f"Contact Information : "
        f"{result['contact_score']:.2f}%"
    )

    print(
        f"Formatting Score    : "
        f"{result['formatting_score']:.2f}%"
    )

    print(
        f"Resume Length       : "
        f"{result['length_score']:.2f}%"
    )


    print("\n" + "-" * 50)


    print(
        f"ATS SCORE: "
        f"{result['ats_score']:.2f}/100"
    )


    print("\n" + "=" * 70)
    print("DETECTED ATS KEYWORDS")
    print("=" * 70)


    for keyword in result["keywords"]:

        print(
            "✓",
            keyword
        )


    print("\n" + "=" * 70)
    print("DETECTED RESUME SECTIONS")
    print("=" * 70)


    for section in result["sections"]:

        print(
            "✓",
            section.title()
        )


    print("\n" + "=" * 70)
    print("ATS ANALYSIS COMPLETED")
    print("=" * 70)