import re

from agent.sparql_engine import (
    get_departments,
    get_subjects,
    get_faculty,
    get_students,
    get_faculty_by_subject,
    get_subjects_by_faculty,
    get_subjects_by_department,
    get_course_subjects,
    get_prerequisites,
    get_student_by_roll_number,
    get_subject_details,
)


def normalize_question(question):
    """
    Normalize the user's question so that different
    capitalization and spacing styles are handled consistently.
    """
    if question is None:
        return ""

    return " ".join(
        str(question).lower().strip().split()
    )


def find_subject(question):
    """
    Find a subject mentioned in the user's question.
    Longer subject names are checked first so that
    specific names are matched correctly.
    """
    subjects = get_subjects()

    question_lower = normalize_question(question)

    subjects = sorted(
        subjects,
        key=lambda item: len(item["name"]),
        reverse=True,
    )

    for subject in subjects:
        subject_name = subject["name"]

        if subject_name.lower() in question_lower:
            return subject_name

        # Handle common short forms.
        aliases = {
            "artificial intelligence": [
                "ai",
                "artificial intelligence",
            ],
            "machine learning": [
                "ml",
                "machine learning",
            ],
            "database management systems": [
                "dbms",
                "database",
                "database management",
                "database management systems",
            ],
            "data structures": [
                "data structure",
                "data structures",
                "ds",
            ],
            "computer networks": [
                "computer network",
                "computer networks",
                "cn",
            ],
            "operating systems": [
                "operating system",
                "operating systems",
                "os",
            ],
            "java programming": [
                "java",
                "java programming",
            ],
            "web technology": [
                "web technology",
                "web technologies",
                "web tech",
            ],
        }

        subject_aliases = aliases.get(
            subject_name.lower(),
            [],
        )

        for alias in subject_aliases:
            if alias in question_lower:
                return subject_name

    return None


def find_faculty(question):
    """
    Find a faculty member mentioned in the question.
    Supports full names and meaningful parts of names.
    """
    faculty_list = get_faculty()

    question_lower = normalize_question(question)

    for faculty in faculty_list:
        full_name = faculty["name"]

        if full_name.lower() in question_lower:
            return full_name

        clean_name = (
            full_name.lower()
            .replace(".", "")
        )

        parts = clean_name.split()

        for part in parts:
            if len(part) > 3 and part in question_lower:
                return full_name

    return None


def find_department(question):
    """
    Find a department mentioned in the question.
    Also supports common abbreviations.
    """
    departments = get_departments()

    question_lower = normalize_question(question)

    departments = sorted(
        departments,
        key=lambda item: len(item["name"]),
        reverse=True,
    )

    aliases = {
        "information technology": [
            "information technology",
            "it",
            "information tech",
        ],
        "computer engineering": [
            "computer engineering",
            "computer engg",
            "ce",
        ],
        "artificial intelligence and data science": [
            "artificial intelligence and data science",
            "artificial intelligence",
            "ai and ds",
            "ai&ds",
            "aids",
            "ai ds",
            "data science",
        ],
        "mechanical engineering": [
            "mechanical engineering",
            "mechanical",
            "me",
        ],
        "electronics and telecommunication engineering": [
            "electronics and telecommunication engineering",
            "electronics and telecommunication",
            "electronics",
            "telecommunication",
            "entc",
            "e&tc",
            "e and tc",
        ],
    }

    for department in departments:
        department_name = department["name"]

        if department_name.lower() in question_lower:
            return department_name

        department_aliases = aliases.get(
            department_name.lower(),
            [],
        )

        for alias in department_aliases:
            if alias in question_lower:
                return department_name

    return None


def find_roll_number(question):
    """
    Extract a student roll number from natural language.
    Examples:
        student 53
        roll 53
        roll number 53
        tell me about 53
    """
    question_lower = normalize_question(question)

    patterns = [
        r"\broll\s*number\s*(\d{2,4})\b",
        r"\broll\s*(\d{2,4})\b",
        r"\bstudent\s*(\d{2,4})\b",
        r"\b(?:about|details\s+of|information\s+about)\s+student\s*(\d{2,4})\b",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            question_lower,
        )

        if match:
            return match.group(1)

    return None


def format_list(items, field="name"):
    """
    Convert query results into a readable comma-separated list.
    """
    if not items:
        return "No information found."

    values = []

    for item in items:
        value = item.get(field)

        if value is not None:
            values.append(str(value))

    if not values:
        return "No information found."

    return ", ".join(values)


def is_department_question(normalized):
    """
    Detect questions asking about college branches/departments.
    """
    department_keywords = [
        "department",
        "departments",
        "branch",
        "branches",
        "stream",
        "streams",
        "field",
        "fields",
        "engineering branch",
    ]

    listing_keywords = [
        "offer",
        "offers",
        "offered",
        "available",
        "have",
        "has",
        "provide",
        "provides",
        "provided",
        "list",
        "which",
        "what",
        "all",
    ]

    return (
        any(
            keyword in normalized
            for keyword in department_keywords
        )
        and any(
            keyword in normalized
            for keyword in listing_keywords
        )
    )


def is_subject_listing_question(normalized):
    """
    Detect questions asking for a general list of subjects.
    """
    subject_words = [
        "subject",
        "subjects",
    ]

    listing_words = [
        "list",
        "which",
        "what",
        "all",
        "available",
        "offer",
        "offered",
        "have",
        "contains",
    ]

    return (
        any(
            word in normalized
            for word in subject_words
        )
        and any(
            word in normalized
            for word in listing_words
        )
    )


def is_faculty_listing_question(normalized):
    """
    Detect questions asking for a general faculty list.
    """
    faculty_words = [
        "faculty",
        "teachers",
        "teaching staff",
        "professors",
    ]

    listing_words = [
        "list",
        "who",
        "all",
        "available",
        "have",
        "which",
    ]

    return (
        any(
            word in normalized
            for word in faculty_words
        )
        and any(
            word in normalized
            for word in listing_words
        )
    )


def ask_agent(question):
    """
    Main natural-language question answering function.

    The function detects the user's intent, extracts relevant
    ontology entities, calls the SPARQL layer, and produces
    a structured answer for the FastAPI backend.
    """
    normalized = normalize_question(question)

    if not normalized:
        return {
            "question": question,
            "answer": "Please enter a question.",
            "type": "error",
            "data": [],
        }

    # Detect important entities once.
    faculty_name = find_faculty(normalized)
    subject = find_subject(normalized)
    department = find_department(normalized)
    roll_number = find_roll_number(normalized)

    # ==========================================================
    # 1. STUDENT / ROLL NUMBER
    # ==========================================================

    if roll_number and (
        "student" in normalized
        or "roll" in normalized
        or "enrolled" in normalized
        or "about" in normalized
        or "details" in normalized
        or "information" in normalized
    ):
        student = get_student_by_roll_number(
            roll_number
        )

        if student:
            data = student[0]

            answer = (
                f"{data['name']} has roll number "
                f"{roll_number}, belongs to the "
                f"{data['department']} department, "
                f"and is enrolled in "
                f"{data['course']}."
            )

            return {
                "question": question,
                "answer": answer,
                "type": "student",
                "data": student,
            }

        return {
            "question": question,
            "answer": (
                f"No student with roll number "
                f"{roll_number} was found."
            ),
            "type": "student",
            "data": [],
        }

    # ==========================================================
    # 2. FACULTY WHO TEACHES A SUBJECT
    # ==========================================================

    if subject and (
        "who teaches" in normalized
        or "who teach" in normalized
        or "who is teaching" in normalized
        or "who teaches" in normalized
        or "faculty teaches" in normalized
        or "faculty teach" in normalized
        or "teacher" in normalized
        or "teachers" in normalized
    ):
        faculty = get_faculty_by_subject(
            subject
        )

        if faculty:
            names = [
                item["name"]
                for item in faculty
            ]

            return {
                "question": question,
                "answer": (
                    f"The faculty teaching "
                    f"{subject} are: "
                    + ", ".join(names)
                ),
                "type": "faculty_by_subject",
                "data": faculty,
            }

        return {
            "question": question,
            "answer": (
                f"No faculty information was "
                f"found for {subject}."
            ),
            "type": "faculty_by_subject",
            "data": [],
        }

    # ==========================================================
    # 3. SUBJECTS TAUGHT BY FACULTY
    # ==========================================================

    if faculty_name and (
        "subject" in normalized
        or "teaches" in normalized
        or "teach" in normalized
        or "teaching" in normalized
        or "handles" in normalized
        or "handle" in normalized
        or "takes" in normalized
        or "take" in normalized
    ):
        subjects = get_subjects_by_faculty(
            faculty_name
        )

        if subjects:
            return {
                "question": question,
                "answer": (
                    f"{faculty_name} teaches: "
                    + format_list(subjects)
                ),
                "type": "subjects_by_faculty",
                "data": subjects,
            }

        return {
            "question": question,
            "answer": (
                f"No subjects were found "
                f"for {faculty_name}."
            ),
            "type": "subjects_by_faculty",
            "data": [],
        }

    # ==========================================================
    # 4. SUBJECT PREREQUISITE
    # ==========================================================

    if subject and (
        "prerequisite" in normalized
        or "prerequisites" in normalized
        or "requirement" in normalized
        or "requirements" in normalized
        or "before taking" in normalized
        or "need before" in normalized
        or "required before" in normalized
    ):
        prerequisites = get_prerequisites(
            subject
        )

        if prerequisites:
            return {
                "question": question,
                "answer": (
                    f"The prerequisite for "
                    f"{subject} is "
                    + format_list(prerequisites)
                ),
                "type": "prerequisite",
                "data": prerequisites,
            }

        return {
            "question": question,
            "answer": (
                f"No prerequisite information "
                f"was found for {subject}."
            ),
            "type": "prerequisite",
            "data": [],
        }

    # ==========================================================
    # 5. SUBJECT DETAILS
    # ==========================================================

    if subject and (
        "details" in normalized
        or "information" in normalized
        or "credits" in normalized
        or "credit" in normalized
        or "laboratory" in normalized
        or "lab" in normalized
        or "classroom" in normalized
        or "room" in normalized
        or "semester" in normalized
        or "tell me about" in normalized
        or "about" in normalized
    ):
        details = get_subject_details(
            subject
        )

        if details:
            data = details[0]

            answer = (
                f"{data['name']} has "
                f"{data['credits']} credits, "
                f"is offered in "
                f"{data['semester']}, "
                f"and uses {data['classroom']}"
            )

            if data["laboratory"]:
                answer += (
                    f", with {data['laboratory']}"
                )

            answer += "."

            return {
                "question": question,
                "answer": answer,
                "type": "subject_details",
                "data": details,
            }

        return {
            "question": question,
            "answer": (
                f"No details were found "
                f"for {subject}."
            ),
            "type": "subject_details",
            "data": [],
        }

    # ==========================================================
    # 6. SUBJECTS BY DEPARTMENT / BRANCH
    # ==========================================================

    if department and (
        "subject" in normalized
        or "course" in normalized
        or "branch" in normalized
        or "department" in normalized
    ):
        subjects = get_subjects_by_department(
            department
        )

        return {
            "question": question,
            "answer": (
                f"The subjects offered by "
                f"{department} are: "
                + format_list(subjects)
            ),
            "type": "subjects_by_department",
            "data": subjects,
        }

    # ==========================================================
    # 7. GENERAL DEPARTMENT / BRANCH LIST
    # ==========================================================

    if is_department_question(normalized):
        departments = get_departments()

        return {
            "question": question,
            "answer": (
                "The college offers the following "
                "departments/branches: "
                + format_list(departments)
            ),
            "type": "departments",
            "data": departments,
        }

    # ==========================================================
    # 8. COURSE SUBJECTS
    # ==========================================================

    if "course" in normalized and (
        "subject" in normalized
        or "contains" in normalized
        or "include" in normalized
        or "includes" in normalized
        or "study" in normalized
        or "taught" in normalized
    ):
        subjects = get_course_subjects(
            "B.Tech Information Technology"
        )

        return {
            "question": question,
            "answer": (
                "B.Tech Information Technology "
                "contains the following subjects: "
                + format_list(subjects)
            ),
            "type": "course_subjects",
            "data": subjects,
        }

    # ==========================================================
    # 9. GENERAL FACULTY LIST
    # ==========================================================

    if is_faculty_listing_question(
        normalized
    ) and not faculty_name:
        faculty = get_faculty()

        names = [
            item["name"]
            for item in faculty
        ]

        return {
            "question": question,
            "answer": (
                "The faculty members are: "
                + ", ".join(names)
            ),
            "type": "faculty",
            "data": faculty,
        }

    # ==========================================================
    # 10. GENERAL SUBJECT LIST
    # ==========================================================

    if (
        is_subject_listing_question(normalized)
        and not faculty_name
        and not department
        and not subject
    ):
        subjects = get_subjects()

        return {
            "question": question,
            "answer": (
                "The available subjects are: "
                + format_list(subjects)
            ),
            "type": "subjects",
            "data": subjects,
        }

    # ==========================================================
    # 11. DIRECT SUBJECT QUESTION
    # ==========================================================

    if subject and (
        "what is" in normalized
        or "what are" in normalized
        or "tell me about" in normalized
        or "about" in normalized
    ):
        details = get_subject_details(
            subject
        )

        if details:
            data = details[0]

            answer = (
                f"{data['name']} has "
                f"{data['credits']} credits, "
                f"is offered in "
                f"{data['semester']}, "
                f"and uses {data['classroom']}"
            )

            if data["laboratory"]:
                answer += (
                    f", with {data['laboratory']}"
                )

            answer += "."

            return {
                "question": question,
                "answer": answer,
                "type": "subject_details",
                "data": details,
            }

    # ==========================================================
    # 12. UNKNOWN QUESTION
    # ==========================================================

    return {
        "question": question,
        "answer": (
            "I could not understand the question. "
            "Try asking about departments, branches, "
            "subjects, faculty, students, prerequisites, "
            "courses, or subject details."
        ),
        "type": "unknown",
        "data": [],
    }