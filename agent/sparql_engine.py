from pathlib import Path

from rdflib import Graph, Literal


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ONTOLOGY_FILE = BASE_DIR / "ontology" / "college_ontology.ttl"
DATA_FILE = BASE_DIR / "ontology" / "college_data.ttl"


# ============================================================
# GRAPH LOADER
# ============================================================

def load_knowledge_graph():
    """
    Load the college ontology and college data
    into a single RDF graph.
    """

    graph = Graph()

    graph.parse(ONTOLOGY_FILE, format="turtle")
    graph.parse(DATA_FILE, format="turtle")

    return graph


# ============================================================
# HELPER
# ============================================================

def normalize_text(value):
    """
    Convert user input into a clean string.
    """

    return str(value).strip()


# ============================================================
# 1. GET DEPARTMENTS
# ============================================================

def get_departments():
    """
    Return all departments in the college.
    """

    graph = load_knowledge_graph()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?department ?name
    WHERE {
        ?department a :Department ;
                    :hasName ?name .
    }
    ORDER BY ?name
    """

    results = graph.query(query)

    departments = []

    for row in results:
        departments.append({
            "id": str(row.department),
            "name": str(row.name)
        })

    return departments


# ============================================================
# 2. GET SUBJECTS
# ============================================================

def get_subjects():
    """
    Return all subjects in the college.
    """

    graph = load_knowledge_graph()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?subject ?name
    WHERE {
        ?subject a :Subject ;
                 :hasName ?name .
    }
    ORDER BY ?name
    """

    results = graph.query(query)

    subjects = []

    for row in results:
        subjects.append({
            "id": str(row.subject),
            "name": str(row.name)
        })

    return subjects


# ============================================================
# 3. GET FACULTY
# ============================================================

def get_faculty():
    """
    Return all faculty members.
    """

    graph = load_knowledge_graph()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?faculty ?name ?departmentName
    WHERE {
        ?faculty a :Faculty ;
                 :hasName ?name ;
                 :belongsToDepartment ?department .

        ?department :hasName ?departmentName .
    }
    ORDER BY ?name
    """

    results = graph.query(query)

    faculty = []

    for row in results:
        faculty.append({
            "id": str(row.faculty),
            "name": str(row.name),
            "department": str(row.departmentName)
        })

    return faculty


# ============================================================
# 4. GET STUDENTS
# ============================================================

def get_students():
    """
    Return all students.
    """

    graph = load_knowledge_graph()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?student ?name ?rollNumber ?departmentName
    WHERE {
        ?student a :Student ;
                 :hasName ?name ;
                 :hasRollNumber ?rollNumber ;
                 :belongsToDepartment ?department .

        ?department :hasName ?departmentName .
    }
    ORDER BY ?rollNumber
    """

    results = graph.query(query)

    students = []

    for row in results:
        students.append({
            "id": str(row.student),
            "name": str(row.name),
            "rollNumber": str(row.rollNumber),
            "department": str(row.departmentName)
        })

    return students


# ============================================================
# 5. GET SUBJECTS TAUGHT BY FACULTY
# ============================================================

def get_subjects_by_faculty(faculty_name):
    """
    Find subjects taught by a faculty member.

    Example:
        get_subjects_by_faculty("Rajendra")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(faculty_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?subject ?subjectName
    WHERE {
        ?faculty a :Faculty ;
                 :hasName ?facultyName ;
                 :teaches ?subject .

        ?subject :hasName ?subjectName .

        FILTER(
            CONTAINS(
                LCASE(STR(?facultyName)),
                ?searchName
            )
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    subjects = []

    for row in results:
        subjects.append({
            "id": str(row.subject),
            "name": str(row.subjectName)
        })

    return subjects


# ============================================================
# 6. GET FACULTY TEACHING A SUBJECT
# ============================================================

def get_faculty_by_subject(subject_name):
    """
    Find faculty members who teach a subject.

    Example:
        get_faculty_by_subject("Artificial Intelligence")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(subject_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?faculty ?facultyName ?departmentName
    WHERE {
        ?faculty a :Faculty ;
                 :hasName ?facultyName ;
                 :teaches ?subject ;
                 :belongsToDepartment ?department .

        ?subject :hasName ?subjectName .

        ?department :hasName ?departmentName .

        FILTER(
            CONTAINS(
                LCASE(STR(?subjectName)),
                ?searchName
            )
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    faculty = []

    for row in results:
        faculty.append({
            "id": str(row.faculty),
            "name": str(row.facultyName),
            "department": str(row.departmentName)
        })

    return faculty


# ============================================================
# 7. GET SUBJECTS BY DEPARTMENT
# ============================================================

def get_subjects_by_department(department_name):
    """
    Find subjects offered by a department.

    Example:
        get_subjects_by_department("Information Technology")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(department_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT DISTINCT ?subject ?subjectName
    WHERE {
        ?department a :Department ;
                    :hasName ?departmentName ;
                    :offersSubject ?subject .

        ?subject :hasName ?subjectName .

        FILTER(
            CONTAINS(
                LCASE(STR(?departmentName)),
                ?searchName
            )
        )
    }
    ORDER BY ?subjectName
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    subjects = []

    for row in results:
        subjects.append({
            "id": str(row.subject),
            "name": str(row.subjectName)
        })

    return subjects


# ============================================================
# 8. GET COURSE SUBJECTS
# ============================================================

def get_course_subjects(course_name):
    """
    Find subjects contained in a course.

    Example:
        get_course_subjects("B.Tech Information Technology")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(course_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?subject ?subjectName
    WHERE {
        ?course a :Course ;
                :hasName ?courseName ;
                :containsSubject ?subject .

        ?subject :hasName ?subjectName .

        FILTER(
            CONTAINS(
                LCASE(STR(?courseName)),
                ?searchName
            )
        )
    }
    ORDER BY ?subjectName
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    subjects = []

    for row in results:
        subjects.append({
            "id": str(row.subject),
            "name": str(row.subjectName)
        })

    return subjects


# ============================================================
# 9. GET PREREQUISITES
# ============================================================

def get_prerequisites(subject_name):
    """
    Find prerequisites of a subject.

    Example:
        get_prerequisites("Machine Learning")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(subject_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?prerequisite ?prerequisiteName
    WHERE {
        ?subject a :Subject ;
                 :hasName ?subjectName ;
                 :hasPrerequisite ?prerequisite .

        ?prerequisite :hasName ?prerequisiteName .

        FILTER(
            CONTAINS(
                LCASE(STR(?subjectName)),
                ?searchName
            )
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    prerequisites = []

    for row in results:
        prerequisites.append({
            "id": str(row.prerequisite),
            "name": str(row.prerequisiteName)
        })

    return prerequisites


# ============================================================
# 10. GET STUDENT BY ROLL NUMBER
# ============================================================

def get_student_by_roll_number(roll_number):
    """
    Find a student using their roll number.

    Example:
        get_student_by_roll_number(53)
    """

    graph = load_knowledge_graph()

    search_roll = str(roll_number).strip()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?student ?name ?departmentName ?courseName
    WHERE {
        ?student a :Student ;
                 :hasName ?name ;
                 :hasRollNumber ?rollNumber ;
                 :belongsToDepartment ?department ;
                 :enrolledIn ?course .

        ?department :hasName ?departmentName .

        ?course :hasName ?courseName .

        FILTER(
            STR(?rollNumber) = ?searchRoll
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchRoll": Literal(search_roll)
        }
    )

    students = []

    for row in results:
        students.append({
            "id": str(row.student),
            "name": str(row.name),
            "department": str(row.departmentName),
            "course": str(row.courseName)
        })

    return students


# ============================================================
# 11. GET SUBJECT DETAILS
# ============================================================

def get_subject_details(subject_name):
    """
    Get detailed information about a subject.

    Example:
        get_subject_details("Artificial Intelligence")
    """

    graph = load_knowledge_graph()

    search_name = normalize_text(subject_name).lower()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT
        ?subject
        ?subjectName
        ?credits
        ?semesterName
        ?classroomName
        ?laboratoryName
    WHERE {

        ?subject a :Subject ;
                 :hasName ?subjectName .

        OPTIONAL {
            ?subject :hasCredits ?credits .
        }

        OPTIONAL {
            ?subject :offeredInSemester ?semester .
            ?semester :hasName ?semesterName .
        }

        OPTIONAL {
            ?subject :usesClassroom ?classroom .
            ?classroom :hasName ?classroomName .
        }

        OPTIONAL {
            ?subject :usesLaboratory ?laboratory .
            ?laboratory :hasName ?laboratoryName .
        }

        FILTER(
            CONTAINS(
                LCASE(STR(?subjectName)),
                ?searchName
            )
        )
    }
    """

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(search_name)
        }
    )

    subjects = []

    for row in results:
        subjects.append({
            "id": str(row.subject),
            "name": str(row.subjectName),
            "credits": str(row.credits) if row.credits else None,
            "semester": str(row.semesterName) if row.semesterName else None,
            "classroom": str(row.classroomName) if row.classroomName else None,
            "laboratory": str(row.laboratoryName) if row.laboratoryName else None
        })

    return subjects