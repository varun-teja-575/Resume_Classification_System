import re


# ============================================================
# GENERAL SKILL DATABASE
# ============================================================

SKILL_LIST = [

    # Programming Languages
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "r",
    "php",

    # Web Development
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "nodejs",
    "express",
    "django",
    "flask",
    "spring",
    "spring boot",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sqlite",
    "redis",

    # Data Science / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "data analysis",
    "natural language processing",
    "nlp",
    "computer vision",

    # Python Libraries
    "numpy",
    "pandas",
    "scikit-learn",
    "sklearn",
    "matplotlib",
    "seaborn",
    "plotly",
    "tensorflow",
    "pytorch",
    "keras",

    # DevOps / Cloud
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "google cloud",
    "jenkins",
    "terraform",

    # Other
    "linux",
    "rest api",
    "restful api",
    "api",
    "microservices",
    "agile",
    "scrum",
    "jira",
    "excel",
    "power bi",
    "tableau"
]


# ============================================================
# ROLE-SPECIFIC REQUIRED SKILLS
# ============================================================

ROLE_SKILLS = {

    "Python Developer": [
        "python",
        "sql",
        "git",
        "django",
        "flask",
        "rest api",
        "docker"
    ],

    "Java Developer": [
        "java",
        "sql",
        "spring boot",
        "git",
        "rest api",
        "docker",
        "mysql"
    ],

    "Data Science": [
        "python",
        "sql",
        "pandas",
        "numpy",
        "machine learning",
        "scikit-learn",
        "matplotlib",
        "data analysis"
    ],

    "Web Designing": [
        "html",
        "css",
        "javascript",
        "react",
        "bootstrap",
        "git"
    ],

    "DevOps Engineer": [
        "linux",
        "git",
        "docker",
        "kubernetes",
        "jenkins",
        "aws",
        "terraform"
    ],

    "Database": [
        "sql",
        "mysql",
        "oracle",
        "postgresql",
        "mongodb"
    ],

    "Testing": [
        "manual testing",
        "automation testing",
        "selenium",
        "java",
        "sql",
        "jira"
    ],

    "Automation Testing": [
        "selenium",
        "java",
        "python",
        "sql",
        "git",
        "jira"
    ],

    "Business Analyst": [
        "sql",
        "excel",
        "power bi",
        "tableau",
        "jira",
        "agile"
    ],

    "Network Security Engineer": [
        "network security",
        "linux",
        "firewall",
        "python",
        "cloud",
        "aws"
    ],

    "SAP Developer": [
        "sap",
        "abap",
        "sql",
        "java"
    ],

    "ETL Developer": [
        "sql",
        "python",
        "etl",
        "oracle",
        "data warehouse"
    ],

    "Blockchain": [
        "blockchain",
        "solidity",
        "ethereum",
        "javascript",
        "web3"
    ],

    "Hadoop": [
        "hadoop",
        "spark",
        "python",
        "java",
        "sql"
    ],

    "DotNet Developer": [
        "c#",
        ".net",
        "asp.net",
        "sql",
        "git",
        "azure"
    ]
}


# ============================================================
# NORMALIZE SKILL
# ============================================================

def normalize_skill(skill):

    return skill.lower().strip()


# ============================================================
# EXTRACT SKILLS
# ============================================================

def extract_skills(resume_text):

    if not resume_text:

        return []

    text = resume_text.lower()

    detected_skills = []


    for skill in SKILL_LIST:

        pattern = re.escape(skill)

        if re.search(
            r"(?<!\w)" + pattern + r"(?!\w)",
            text
        ):

            detected_skills.append(
                normalize_skill(skill)
            )


    # Remove duplicates
    detected_skills = list(
        dict.fromkeys(
            detected_skills
        )
    )


    return detected_skills


# ============================================================
# GET REQUIRED SKILLS FOR ROLE
# ============================================================

def get_required_skills(role):

    if not role:

        return []

    # Exact match
    if role in ROLE_SKILLS:

        return ROLE_SKILLS[role]


    # Case-insensitive match
    role_lower = role.lower()

    for stored_role in ROLE_SKILLS:

        if stored_role.lower() == role_lower:

            return ROLE_SKILLS[stored_role]


    return []


# ============================================================
# FIND MISSING SKILLS
# ============================================================

def find_missing_skills(
    detected_skills,
    role
):

    required_skills = get_required_skills(
        role
    )

    detected_lower = [
        skill.lower()
        for skill in detected_skills
    ]

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in detected_lower:

            missing_skills.append(
                skill
            )


    return missing_skills


# ============================================================
# SKILL MATCH PERCENTAGE
# ============================================================

def calculate_skill_match(
    detected_skills,
    role
):

    required_skills = get_required_skills(
        role
    )

    if not required_skills:

        return 0.0


    detected_lower = [
        skill.lower()
        for skill in detected_skills
    ]


    matched = 0

    for skill in required_skills:

        if skill.lower() in detected_lower:

            matched += 1


    percentage = (
        matched / len(required_skills)
    ) * 100


    return percentage


# ============================================================
# TEST PROGRAM
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RESUME SKILL ANALYZER")
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


    # --------------------------------------------------------
    # Detect skills
    # --------------------------------------------------------

    detected_skills = extract_skills(
        resume_text
    )


    print("\n" + "=" * 70)
    print("DETECTED SKILLS")
    print("=" * 70)


    if detected_skills:

        for skill in detected_skills:

            print(
                "✓",
                skill
            )

    else:

        print(
            "No skills detected."
        )


    print(
        "\nTotal Detected Skills:",
        len(detected_skills)
    )


    # --------------------------------------------------------
    # Ask role
    # --------------------------------------------------------

    role = input(
        "\nEnter predicted job role: "
    )


    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    required_skills = get_required_skills(
        role
    )


    print("\n" + "=" * 70)
    print("REQUIRED SKILLS")
    print("=" * 70)


    if required_skills:

        for skill in required_skills:

            print(
                "•",
                skill
            )

    else:

        print(
            "No predefined skill requirements found for this role."
        )


    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    missing_skills = find_missing_skills(
        detected_skills,
        role
    )


    print("\n" + "=" * 70)
    print("MISSING SKILLS")
    print("=" * 70)


    if missing_skills:

        for skill in missing_skills:

            print(
                "✗",
                skill
            )

    else:

        print(
            "No missing skills!"
        )


    # --------------------------------------------------------
    # Skill match
    # --------------------------------------------------------

    match_percentage = calculate_skill_match(
        detected_skills,
        role
    )


    print("\n" + "=" * 70)
    print("SKILL MATCH")
    print("=" * 70)


    print(
        f"\nSkill Match: {match_percentage:.2f}%"
    )


    print("\n" + "=" * 70)
    print("SKILL ANALYSIS COMPLETED")
    print("=" * 70)