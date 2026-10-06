from pathlib import Path

from rdflib import Graph
from owlrl import DeductiveClosure, OWLRL_Semantics


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ONTOLOGY_FILE = BASE_DIR / "ontology" / "college_ontology.ttl"
DATA_FILE = BASE_DIR / "ontology" / "college_data.ttl"


# ============================================================
# LOAD GRAPH
# ============================================================

def load_reasoned_graph():
    """
    Load the ontology and college data,
    then apply OWL-RL reasoning.
    """

    graph = Graph()

    # Load ontology
    graph.parse(
        ONTOLOGY_FILE,
        format="turtle"
    )

    # Load college data
    graph.parse(
        DATA_FILE,
        format="turtle"
    )

    print("Before reasoning:", len(graph), "triples")

    # Apply OWL-RL reasoning
    DeductiveClosure(
        OWLRL_Semantics
    ).expand(graph)

    print("After reasoning:", len(graph), "triples")

    return graph


# ============================================================
# GET ALL INFERRED TRIPLES
# ============================================================

def get_inferred_triples():
    """
    Return triples generated after OWL reasoning.
    """

    graph = load_reasoned_graph()

    triples = []

    for subject, predicate, object_ in graph:
        triples.append({
            "subject": str(subject),
            "predicate": str(predicate),
            "object": str(object_)
        })

    return triples


# ============================================================
# FIND SUBJECT TYPES
# ============================================================

def get_entity_types(entity_name):
    """
    Find RDF/OWL types associated with an entity.
    """

    graph = load_reasoned_graph()

    query = """
    PREFIX : <http://example.org/college#>

    SELECT ?type
    WHERE {
        ?entity a ?type .

        FILTER(
            CONTAINS(
                LCASE(STR(?entity)),
                ?searchName
            )
        )
    }
    """

    from rdflib import Literal

    results = graph.query(
        query,
        initBindings={
            "searchName": Literal(
                entity_name.strip().lower()
            )
        }
    )

    types = []

    for row in results:
        types.append(str(row.type))

    return types


# ============================================================
# COUNT TRIPLES
# ============================================================

def get_triple_counts():
    """
    Compare graph size before and after reasoning.
    """

    graph = Graph()

    graph.parse(
        ONTOLOGY_FILE,
        format="turtle"
    )

    graph.parse(
        DATA_FILE,
        format="turtle"
    )

    before = len(graph)

    DeductiveClosure(
        OWLRL_Semantics
    ).expand(graph)

    after = len(graph)

    return {
        "before_reasoning": before,
        "after_reasoning": after,
        "inferred_triples": after - before
    }