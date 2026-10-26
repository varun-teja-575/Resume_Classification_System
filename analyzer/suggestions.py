# ============================================================
# RESUME IMPROVEMENT SUGGESTIONS
# ============================================================


def generate_suggestions(
    resume_text,
    predicted_role,
    detected_skills,
    missing_skills,
    resume_score,
    ats_result
):

    suggestions = []

    text = resume_text.lower()


    # ========================================================
    # 1. MISSING SKILLS
    # ========================================================

    if missing_skills:

        for skill in missing_skills[:5]:

            suggestions.append(
                f"Consider adding or learning {skill} "
                f"for the {predicted_role} role."
            )


    # ========================================================
    # 2. RESUME SCORE
    # ========================================================

    if resume_score <= 40:

        suggestions.append(
            "Your overall resume score is low. "
            "Consider adding more relevant skills, "
            "projects, certifications and experience."
        )

    elif resume_score <= 60:

        suggestions.append(
            "Your resume has room for improvement. "
            "Add more relevant technical skills and projects."
        )

    elif resume_score <= 80:

        suggestions.append(
            "Your resume is good, but adding more "
            "relevant achievements and skills can improve it."
        )


    # ========================================================
    # 3. ATS SCORE
    # ========================================================

    ats_score = ats_result.get(
        "ats_score",
        0
    )


    if ats_score < 50:

        suggestions.append(
            "Your ATS score is low. "
            "Use clear section headings and "
            "job-relevant keywords."
        )

    elif ats_score < 70:

        suggestions.append(
            "Improve your ATS score by adding "
            "more role-specific keywords."
        )


    # ========================================================
    # 4. CONTACT INFORMATION
    # ========================================================

    contact_score = ats_result.get(
        "contact_score",
        0
    )


    if contact_score == 0:

        suggestions.append(
            "Add your email address and phone number "
            "to the resume."
        )

    elif contact_score < 100:

        suggestions.append(
            "Make sure both your email address and "
            "phone number are clearly visible."
        )


    # ========================================================
    # 5. PROJECTS
    # ========================================================

    if "project" not in text:

        suggestions.append(
            "Add a Projects section with "
            "2–3 relevant academic or personal projects."
        )


    # ========================================================
    # 6. EDUCATION
    # ========================================================

    education_words = [
        "education",
        "b.tech",
        "btech",
        "b.e",
        "bachelor",
        "degree",
        "university",
        "college"
    ]


    education_found = any(
        word in text
        for word in education_words
    )


    if not education_found:

        suggestions.append(
            "Add a clear Education section "
            "with your degree and university."
        )


    # ========================================================
    # 7. CERTIFICATIONS
    # ========================================================

    certification_words = [
        "certification",
        "certificate",
        "certified"
    ]


    certification_found = any(
        word in text
        for word in certification_words
    )


    if not certification_found:

        suggestions.append(
            "Consider adding relevant certifications "
            "to strengthen your profile."
        )


    # ========================================================
    # 8. GITHUB
    # ========================================================

    if "github" not in text:

        suggestions.append(
            "Add your GitHub profile to showcase "
            "your projects and coding experience."
        )


    # ========================================================
    # 9. LINKEDIN
    # ========================================================

    if "linkedin" not in text:

        suggestions.append(
            "Consider adding your LinkedIn profile "
            "to make your professional profile easier to find."
        )


    # ========================================================
    # 10. EXPERIENCE
    # ========================================================

    experience_words = [
        "experience",
        "internship",
        "intern",
        "employment"
    ]


    experience_found = any(
        word in text
        for word in experience_words
    )


    if not experience_found:

        suggestions.append(
            "Add internship, work experience or "
            "relevant practical experience if available."
        )


    # ========================================================
    # 11. SKILLS
    # ========================================================

    if len(detected_skills) < 5:

        suggestions.append(
            "Add more relevant technical skills "
            "to improve your skill coverage."
        )


    # ========================================================
    # 12. RESUME LENGTH
    # ========================================================

    word_count = len(
        resume_text.split()
    )


    if word_count < 150:

        suggestions.append(
            "Your resume appears too short. "
            "Add meaningful project, education and "
            "experience details."
        )


    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    suggestions = list(
        dict.fromkeys(
            suggestions
        )
    )


    return suggestions


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESUME IMPROVEMENT SUGGESTION TEST")
    print("=" * 70)


    resume_text = """

    Java Developer

    Skills:
    Java
    JavaScript
    SQL
    MySQL
    Spring Boot
    Git
    Docker

    Projects:
    Developed a web application using Java.

    Education:
    B.Tech Computer Science

    Certifications:
    Java Certification

    Experience:
    Internship

    """


    predicted_role = "Java Developer"

    detected_skills = [
        "java",
        "javascript",
        "sql",
        "mysql",
        "spring boot",
        "git",
        "docker"
    ]


    missing_skills = [
        "rest api",
        "aws"
    ]


    resume_score = 75


    ats_result = {

        "ats_score": 65,

        "contact_score": 0

    }


    suggestions = generate_suggestions(

        resume_text,

        predicted_role,

        detected_skills,

        missing_skills,

        resume_score,

        ats_result

    )


    print("\n")
    print("=" * 70)
    print("IMPROVEMENT SUGGESTIONS")
    print("=" * 70)


    if suggestions:

        for i, suggestion in enumerate(
            suggestions,
            start=1
        ):

            print(
                f"\n{i}. {suggestion}"
            )

    else:

        print(
            "\nYour resume looks good!"
        )


    print("\n" + "=" * 70)
    print("SUGGESTION GENERATION COMPLETED")
    print("=" * 70)