import re


# ============================================================
# SCORE WEIGHTS
# ============================================================

SCORE_WEIGHTS = {
    "skills": 40,
    "projects": 25,
    "education": 15,
    "certifications": 10,
    "experience": 10
}


# ============================================================
# KEYWORDS
# ============================================================

SKILL_KEYWORDS = [
    "python",
    "java",
    "c++",
    "c#",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "react",
    "angular",
    "node",
    "django",
    "flask",
    "spring",
    "spring boot",
    "machine learning",
    "deep learning",
    "data science",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "kubernetes",
    "html",
    "css"
]


PROJECT_KEYWORDS = [
    "project",
    "projects",
    "developed",
    "built",
    "created",
    "implemented",
    "application",
    "system",
    "website",
    "model"
]


EDUCATION_KEYWORDS = [
    "education",
    "b.tech",
    "btech",
    "b.e",
    "be ",
    "bachelor",
    "m.tech",
    "mtech",
    "mca",
    "master",
    "degree",
    "university",
    "college"
]


CERTIFICATION_KEYWORDS = [
    "certification",
    "certifications",
    "certificate",
    "certified",
    "coursera",
    "udemy",
    "nptel",
    "aws certified",
    "microsoft certified"
]


EXPERIENCE_KEYWORDS = [
    "experience",
    "work experience",
    "professional experience",
    "internship",
    "intern",
    "worked",
    "employment",
    "developer",
    "engineer"
]


# ============================================================
# COUNT SKILLS
# ============================================================

def count_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILL_KEYWORDS:

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills


# ============================================================
# SKILL SCORE
# ============================================================

def calculate_skill_score(text):

    skills = count_skills(text)

    max_skills = 8

    score = (
        min(len(skills), max_skills)
        / max_skills
    ) * SCORE_WEIGHTS["skills"]

    return round(score, 2), skills


# ============================================================
# PROJECT SCORE
# ============================================================

def calculate_project_score(text):

    text = text.lower()

    project_count = 0

    for keyword in PROJECT_KEYWORDS:

        project_count += len(
            re.findall(
                r"\b" + re.escape(keyword) + r"\b",
                text
            )
        )

    if project_count >= 8:

        score = 25

    elif project_count >= 5:

        score = 20

    elif project_count >= 3:

        score = 15

    elif project_count >= 1:

        score = 8

    else:

        score = 0

    return score


# ============================================================
# EDUCATION SCORE
# ============================================================

def calculate_education_score(text):

    text = text.lower()

    found = False

    for keyword in EDUCATION_KEYWORDS:

        if keyword in text:

            found = True

            break

    if found:

        return SCORE_WEIGHTS["education"]

    return 0


# ============================================================
# CERTIFICATION SCORE
# ============================================================

def calculate_certification_score(text):

    text = text.lower()

    certification_count = 0

    for keyword in CERTIFICATION_KEYWORDS:

        certification_count += text.count(
            keyword
        )

    if certification_count >= 3:

        return 10

    elif certification_count == 2:

        return 8

    elif certification_count == 1:

        return 5

    return 0


# ============================================================
# EXPERIENCE SCORE
# ============================================================

def calculate_experience_score(text):

    text = text.lower()

    experience_found = False

    for keyword in EXPERIENCE_KEYWORDS:

        if keyword in text:

            experience_found = True

            break

    if not experience_found:

        return 0


    # Look for years of experience
    year_pattern = r"(\d+)\+?\s*(year|years)"

    years = re.findall(
        year_pattern,
        text
    )


    if years:

        max_years = max(
            int(year[0])
            for year in years
        )

        if max_years >= 3:

            return 10

        elif max_years >= 2:

            return 8

        elif max_years >= 1:

            return 6


    # Internship / basic experience
    if "internship" in text or "intern" in text:

        return 5

    return 4


# ============================================================
# COMPLETE RESUME SCORE
# ============================================================

def calculate_resume_score(text):

    if not text:

        return {
            "skills": 0,
            "projects": 0,
            "education": 0,
            "certifications": 0,
            "experience": 0,
            "total": 0
        }


    skill_score, detected_skills = (
        calculate_skill_score(text)
    )

    project_score = (
        calculate_project_score(text)
    )

    education_score = (
        calculate_education_score(text)
    )

    certification_score = (
        calculate_certification_score(text)
    )

    experience_score = (
        calculate_experience_score(text)
    )


    total_score = (
        skill_score
        + project_score
        + education_score
        + certification_score
        + experience_score
    )


    total_score = min(
        round(total_score, 2),
        100
    )


    return {
        "skills": skill_score,
        "projects": project_score,
        "education": education_score,
        "certifications": certification_score,
        "experience": experience_score,
        "total": total_score,
        "detected_skills": detected_skills
    }


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESUME SCORE CALCULATOR")
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


    result = calculate_resume_score(
        resume_text
    )


    print("\n" + "=" * 70)
    print("RESUME SCORE")
    print("=" * 70)

    print(
        f"\nSkills          : "
        f"{result['skills']}/40"
    )

    print(
        f"Projects        : "
        f"{result['projects']}/25"
    )

    print(
        f"Education       : "
        f"{result['education']}/15"
    )

    print(
        f"Certifications  : "
        f"{result['certifications']}/10"
    )

    print(
        f"Experience      : "
        f"{result['experience']}/10"
    )

    print(
        "\n" + "-" * 40
    )

    print(
        f"TOTAL RESUME SCORE: "
        f"{result['total']}/100"
    )

    print(
        "\nDetected Skills:"
    )

    for skill in result["detected_skills"]:

        print(
            "✓",
            skill
        )

    print("\n" + "=" * 70)
    print("RESUME SCORING COMPLETED")
    print("=" * 70)