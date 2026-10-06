from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rdflib import Graph, RDF, RDFS, OWL

from agent.college_agent import ask_agent
from agent.reasoner import get_triple_counts
from agent.sparql_engine import (
    get_departments,
    get_subjects,
    get_faculty,
    get_students,
    get_course_subjects,
)


BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URI = "http://example.org/college#"

ONTOLOGY_FILE = (
    BASE_DIR
    / "ontology"
    / "college_ontology.ttl"
)

DATA_FILE = (
    BASE_DIR
    / "ontology"
    / "college_data.ttl"
)


app = FastAPI(
    title="College Ontology AI Agent",
    description=(
        "Ontology-based intelligent college knowledge agent "
        "using RDF, SPARQL and OWL-RL reasoning."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str


def local_name(uri):
    """
    Convert an ontology URI into a readable name.
    """

    value = str(uri)

    if "#" in value:
        value = value.split("#")[-1]

    if "/" in value:
        value = value.rstrip("/").split("/")[-1]

    import re

    value = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        value,
    )

    value = value.replace("_", " ")

    return value.strip()


def build_graph_data():
    """
    Build a frontend-friendly representation of the
    actual RDF knowledge graph.
    """

    graph = Graph()

    graph.parse(
        ONTOLOGY_FILE,
        format="turtle",
    )

    graph.parse(
        DATA_FILE,
        format="turtle",
    )

    object_properties = set()

    for subject, predicate, object_ in graph:
        if (
            predicate == RDF.type
            and object_ == OWL.ObjectProperty
        ):
            object_properties.add(str(subject))

    nodes = {}
    edges = []

    for subject, predicate, object_ in graph:

        predicate_uri = str(predicate)

        if predicate_uri not in object_properties:
            continue

        subject_uri = str(subject)
        object_uri = str(object_)

        if not subject_uri.startswith(BASE_URI):
            continue

        if not object_uri.startswith(BASE_URI):
            continue

        source = local_name(subject_uri)
        target = local_name(object_uri)
        relation = local_name(predicate_uri)

        if source not in nodes:
            nodes[source] = {
                "id": source,
                "label": source,
                "type": "entity",
            }

        if target not in nodes:
            nodes[target] = {
                "id": target,
                "label": target,
                "type": "entity",
            }

        edges.append(
            {
                "source": source,
                "target": target,
                "relation": relation,
            }
        )

    for subject, predicate, object_ in graph:

        if predicate != RDF.type:
            continue

        subject_uri = str(subject)
        object_uri = str(object_)

        if not subject_uri.startswith(BASE_URI):
            continue

        if object_uri.startswith(BASE_URI):

            entity_name = local_name(subject_uri)
            class_name = local_name(object_uri)

            if entity_name in nodes:
                nodes[entity_name]["type"] = class_name

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def build_reasoning_data():
    """
    Compare the original RDF graph with the graph after
    OWL-RL reasoning.

    The endpoint intentionally focuses on useful semantic
    inference examples rather than generic owl:Thing facts.
    """

    base_graph = Graph()

    base_graph.parse(
        ONTOLOGY_FILE,
        format="turtle",
    )

    base_graph.parse(
        DATA_FILE,
        format="turtle",
    )

    before_triples = set(base_graph)

    reasoned_graph = Graph()

    reasoned_graph.parse(
        ONTOLOGY_FILE,
        format="turtle",
    )

    reasoned_graph.parse(
        DATA_FILE,
        format="turtle",
    )

    from owlrl import (
        DeductiveClosure,
        OWLRL_Semantics,
    )

    DeductiveClosure(
        OWLRL_Semantics
    ).expand(reasoned_graph)

    after_triples = set(reasoned_graph)

    inferred_triples = (
        after_triples - before_triples
    )

    examples = []

    for subject, predicate, object_ in inferred_triples:

        subject_uri = str(subject)
        predicate_uri = str(predicate)
        object_uri = str(object_)

        if not subject_uri.startswith(BASE_URI):
            continue

        # Skip generic OWL/RDF metadata.
        if predicate in {
            RDF.type,
            RDFS.label,
            RDFS.comment,
        }:
            continue

        if predicate_uri.startswith(
            "http://www.w3.org/"
        ):
            continue

        if not object_uri.startswith(BASE_URI):
            continue

        subject_name = local_name(
            subject_uri
        )

        predicate_name = local_name(
            predicate_uri
        )

        object_name = local_name(
            object_uri
        )

        examples.append(
            {
                "subject": subject_name,
                "predicate": predicate_name,
                "object": object_name,
            }
        )

    unique_examples = []

    seen = set()

    for example in examples:

        key = (
            example["subject"],
            example["predicate"],
            example["object"],
        )

        if key in seen:
            continue

        seen.add(key)
        unique_examples.append(example)

    unique_examples.sort(
        key=lambda item: (
            item["subject"],
            item["predicate"],
            item["object"],
        )
    )

    unique_examples = unique_examples[:20]

    return {
        "before_reasoning": len(
            before_triples
        ),
        "after_reasoning": len(
            after_triples
        ),
        "inferred_triples": len(
            inferred_triples
        ),
        "reasoning_engine": "OWL-RL",
        "ontology_namespace": BASE_URI,
        "examples": unique_examples,
    }


@app.get("/")
def root():
    return {
        "message": (
            "College Ontology AI Agent is running"
        ),
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": (
            "College Ontology AI Agent"
        ),
    }


@app.get("/api")
def api_information():
    return {
        "name": (
            "College Ontology AI Agent"
        ),
        "description": (
            "Ontology-based college question "
            "answering system"
        ),
        "endpoints": {
            "GET /": "API root",
            "GET /health": "Health check",
            "GET /api": "API information",
            "GET /stats": (
                "Knowledge graph and ontology statistics"
            ),
            "GET /graph": (
                "Actual RDF knowledge graph "
                "nodes and relationships"
            ),
            "GET /reasoning": (
                "OWL-RL reasoning statistics "
                "and inferred knowledge"
            ),
            "POST /ask": (
                "Ask a college-related question"
            ),
        },
    }


@app.get("/stats")
def statistics():
    triple_counts = get_triple_counts()

    departments = get_departments()
    subjects = get_subjects()
    faculty = get_faculty()
    students = get_students()

    courses = get_course_subjects(
        "B.Tech Information Technology"
    )

    return {
        "knowledge_graph": {
            "triples": triple_counts[
                "before_reasoning"
            ],
            "reasoned_triples": triple_counts[
                "after_reasoning"
            ],
            "inferred_triples": triple_counts[
                "inferred_triples"
            ],
        },
        "entities": {
            "departments": len(
                departments
            ),
            "subjects": len(
                subjects
            ),
            "faculty": len(
                faculty
            ),
            "students": len(
                students
            ),
            "courses": 1 if courses else 0,
        },
    }


@app.get("/graph")
def graph():
    return build_graph_data()


@app.get("/reasoning")
def reasoning():
    return build_reasoning_data()


@app.post("/ask")
def ask_question(
    request: QuestionRequest,
):
    return ask_agent(
        request.question
    )