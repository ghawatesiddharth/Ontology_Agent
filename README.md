# 🎓 College Ontology AI Agent

An ontology-based intelligent college knowledge system that combines **RDF, OWL, SPARQL, OWL-RL reasoning, natural-language question handling, FastAPI, and React** to provide semantic answers about college information.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [System Architecture](#️-system-architecture)
- [Technology Stack](#️-technology-stack)
- [Ontology Design](#-ontology-design)
- [Example Knowledge](#-example-knowledge)
- [Example Questions](#-example-questions)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running the Backend](#-running-the-backend)
- [Running the Frontend](#-running-the-frontend)
- [OWL-RL Reasoning](#-owl-rl-reasoning)
- [Knowledge Graph Explorer](#-knowledge-graph-explorer)
- [Natural Language Question Handling](#-natural-language-question-handling)
- [Validation](#-validation)
- [Project Goals](#-project-goals)
- [Future Scope](#-future-scope)
- [Author](#-author)
- [License](#-license)

---

## 📖 Project Overview

The College Ontology AI Agent represents college knowledge as a structured semantic knowledge graph.

Users can ask natural-language questions about:

- Departments
- Subjects
- Faculty
- Students
- Courses
- Prerequisites
- Subject details
- Faculty-subject relationships

The system converts the user's question into an ontology-oriented query, retrieves information using SPARQL, and returns a human-readable response.

The project also applies **OWL-RL reasoning** to expand the knowledge graph with logically derived semantic facts.

---

## ✨ Key Features

### 💬 Intelligent Question Answering

The system understands natural-language questions such as:

- Which branches does the college offer?
- What subjects does Rajendra teach?
- Who teaches Artificial Intelligence?
- What is the prerequisite for Machine Learning?
- Tell me about Artificial Intelligence.
- Which subjects are in B.Tech Information Technology?
- Tell me about student 53.

### 🕸️ Semantic Knowledge Graph

College information is represented using RDF triples and ontology classes/properties.

### 🔎 SPARQL Querying

SPARQL is used to retrieve structured information from the RDF knowledge graph.

### 🧠 OWL-RL Reasoning

The system uses the OWL-RL reasoning engine to derive additional semantic facts.

Current reasoning results:

| Metric | Value |
|---|---:|
| Original RDF triples | 268 |
| Reasoned triples | 731 |
| Additional inferred triples | 463 |
| Reasoning engine | OWL-RL |

### 📊 Interactive Knowledge Graph

The React frontend provides:

- Entity search
- RDF relationship exploration
- Semantic relationship visualization
- Ontology statistics
- Reasoning statistics

### 🌐 Web Application

The system contains:

- React frontend
- FastAPI backend
- RDF/OWL ontology
- SPARQL query engine
- OWL-RL reasoning engine

---

## 🏗️ System Architecture

```text
                    User
                      |
                      v
             React Frontend
                      |
                      | HTTP / REST
                      v
              FastAPI Backend
                      |
                      v
             College AI Agent
                      |
             +--------+--------+
             |                 |
             v                 v
       NLP / Intent        SPARQL Engine
       Understanding            |
             |                  v
             |          RDF Knowledge Graph
             |                  |
             |                  v
             |             OWL-RL Reasoner
             |                  |
             +--------+---------+
                      |
                      v
              Human-readable
                   Answer
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, FastAPI, RDFLib, OWLRL, SPARQL, Pydantic, Uvicorn |
| **Frontend** | React, Vite, JavaScript, CSS, Lucide React |
| **Semantic Web** | RDF, OWL, SPARQL, OWL-RL, Turtle (`.ttl`) |

---

## 🧩 Ontology Design

The ontology defines major college entities including:

- College
- Department
- Faculty
- Student
- Course
- Subject
- Classroom
- Laboratory
- Semester
- Event
- Examination
- Club

### Object Properties

Examples include:

`hasDepartment` · `belongsToDepartment` · `hasFaculty` · `hasStudent` · `offersCourse` · `offersSubject` · `teaches` · `enrolledIn` · `containsSubject` · `hasPrerequisite` · `usesClassroom` · `usesLaboratory` · `offeredInSemester` · `conductsEvent` · `hasExamination` · `memberOfClub`

### Datatype Properties

Examples include:

`hasName` · `hasEmail` · `hasRollNumber` · `hasRoomNumber` · `hasCredits` · `hasSemesterNumber`

---

## 📚 Example Knowledge

The current knowledge base contains representative college information including:

### Departments

- Artificial Intelligence and Data Science
- Computer Engineering
- Electronics and Telecommunication Engineering
- Information Technology
- Mechanical Engineering

### Subjects

- Artificial Intelligence
- Computer Networks
- Data Structures
- Database Management Systems
- Java Programming
- Machine Learning
- Operating Systems
- Web Technology

### Students

Students with roll numbers **53–56** are represented in the current project dataset.

### Faculty

The project dataset contains faculty-subject relationships that can be queried through the ontology.

---

## ❓ Example Questions

### Departments

**Question:** Which branches does the college offer?

**Example response:**
> The college offers the following departments/branches: Artificial Intelligence and Data Science, Computer Engineering, Electronics and Telecommunication Engineering, Information Technology, Mechanical Engineering.

### Faculty

**Question:** What subjects does Rajendra teach?

**Example response:**
> Prof. Rajendra Kankrale teaches: Artificial Intelligence, Database Management Systems.

### Subject Faculty

**Question:** Who teaches Artificial Intelligence?

**Example response:**
> The faculty teaching Artificial Intelligence are: Prof. Rajendra Kankrale, Prof. Neha Joshi.

### Prerequisite

**Question:** What is the prerequisite for Machine Learning?

**Example response:**
> The prerequisite for Machine Learning is Artificial Intelligence.

### Student

**Question:** Tell me about student 53

**Example response:**
> Student 53 has roll number 53, belongs to the Information Technology department, and is enrolled in B.Tech Information Technology.

### Subject Details

**Question:** Tell me about Artificial Intelligence

**Example response:**
> Artificial Intelligence has 4 credits, is offered in Semester 7, and uses IT Classroom 101, with Artificial Intelligence Laboratory.

---

## 📁 Project Structure

```text
Ontology_evelopment_agent/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── agent/
│   ├── __init__.py
│   ├── college_agent.py
│   ├── reasoner.py
│   └── sparql_engine.py
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── ontology/
│   ├── college_ontology.ttl
│   └── college_data.ttl
│
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── index.html
    ├── vite.config.js
    │
    └── src/
        ├── App.jsx
        ├── App.css
        ├── index.css
        └── main.jsx
```

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Ontology_evelopment_agent
```

### 2. Create a Python environment

**Windows**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically provides interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### Backend API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | API root |
| `/health` | GET | Health check |
| `/api` | GET | API information |
| `/stats` | GET | Knowledge graph statistics |
| `/graph` | GET | RDF graph data |
| `/reasoning` | GET | OWL-RL reasoning statistics |
| `/ask` | POST | Ask a college-related question |

---

## 🎨 Running the Frontend

Open a **second terminal**:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## 🧠 OWL-RL Reasoning

The project uses OWL-RL semantic reasoning through `owlrl`.

The reasoning process is:

```text
Original RDF Graph
       |
       | OWL-RL Reasoning
       v
Expanded Knowledge Graph
```

Current project results:

```text
Original triples:       268
Reasoned triples:       731
Additional triples:     463
```

The difference is calculated as:

```text
731 - 268 = 463
```

The inferred-triple count represents the graph expansion produced by the OWL-RL reasoning process.

---

## 🔍 Knowledge Graph Explorer

The frontend provides a technical knowledge graph view where users can:

- Search entities
- Select entities
- Inspect RDF relationships
- View entity types
- Explore relationships between college concepts

This provides a visual demonstration of the underlying semantic model.

---

## 🗣️ Natural Language Question Handling

The agent performs lightweight natural-language question understanding.

The general processing flow is:

```text
Natural-language question
          |
          v
Text normalization
          |
          v
Entity detection
          |
          v
Intent detection
          |
          v
SPARQL query
          |
          v
RDF knowledge graph
          |
          v
Human-readable response
```

This allows users to interact with the ontology using natural-language questions instead of manually writing SPARQL queries.

### Example Query Flow

For the question:

> Who teaches Artificial Intelligence?

The system identifies:

| Component | Value |
|---|---|
| **Entity** | Artificial Intelligence |
| **Intent** | Faculty teaching the subject |

The SPARQL engine then retrieves the corresponding faculty from the ontology, and the final response is presented in natural language.

---

## ✅ Validation

The backend has been tested for:

```text
ROOT       → 200
HEALTH     → 200
STATS      → 200
GRAPH      → 200
REASONING  → 200
```

The frontend is built using:

```bash
npm run build
```

---

## 🎯 Project Goals

The project demonstrates how semantic web technologies can be used to build an intelligent college information system.

The primary goals are:

1. Represent college knowledge using ontology concepts.
2. Store information as RDF triples.
3. Retrieve information using SPARQL.
4. Accept natural-language questions.
5. Apply OWL-RL semantic reasoning.
6. Present the knowledge graph through an interactive web interface.

---

## 🔮 Future Scope

Possible future improvements include:

- More advanced NLP models
- Expanded college ontology
- Additional student and faculty information
- More complex SPARQL queries
- Multi-hop reasoning
- Voice-based interaction
- Authentication
- Persistent conversation history
- Deployment to a cloud platform
- Integration with additional college information systems

---

## 👨‍💻 Author

**Siddharth Ghawate**
College Ontology AI Agent - B.Tech Project

---

## 📜 License

This project is developed for academic and educational purposes.