from neo4j import GraphDatabase
import os
import re

# Configuration Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Sonatel2025")


def run_query(query: str):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]


# === 🔍 Cas source / cible ===
def build_graph_json(question: str):
    match = re.search(r"table\s+(\w+)", question.lower())
    if not match:
        return {"error": "Aucune table reconnue dans la question."}

    table = match.group(1)

    query = f"""
    MATCH (src:Table)-[:FEED]->(t:Table {{nom_table: '{table}'}})
    RETURN src.nom_table AS source, t.nom_table AS target
    UNION
    MATCH (t:Table {{nom_table: '{table}'}})-[:FEED]->(dst:Table)
    RETURN t.nom_table AS source, dst.nom_table AS target
    """

    data = run_query(query)
    if not data:
        return {"nodes": [], "edges": []}

    nodes = set()
    edges = []
    for row in data:
        nodes.add(row["source"])
        nodes.add(row["target"])
        edges.append({"from": row["source"], "to": row["target"]})

    return {
        "nodes": [{"id": n, "label": n} for n in nodes],
        "edges": edges
    }


# === 📊 Cas exhaustivité ===
def check_exhaustivite(question: str):
    match = re.search(r"table\s+(\w+)", question.lower())
    if not match:
        return {"error": "Aucune table reconnue dans la question."}

    table = match.group(1)
    if not table.startswith("trusted_"):
        table = f"trusted_{table}"

    query = f"""
    MATCH (e:Exhaustivite {{nom_table: '{table}'}})
    RETURN e.date_stat AS date, e.etat AS etat
    ORDER BY e.date_stat DESC
    LIMIT 1
    """

    data = run_query(query)
    if not data:
        return {"error": f"Aucune donnée d’exhaustivité trouvée pour {table}"}

    etat = data[0]["etat"]
    color = "green" if etat == "exhaustive" else "red"

    return {
        "nodes": [{"id": table, "label": table, "color": color}],
        "edges": [],
        "etat": etat
    }


# === 📚 Métadonnées générales (hors graphe) ===
def ask_neo4j(question: str):
    match = re.search(r"table\s+(\w+)", question.lower())
    if not match:
        return "Je n'ai pas trouvé de nom de table dans ta question."

    table = match.group(1)
    question_lower = question.lower()

    if "source" in question_lower or "cible" in question_lower:
        return "Utilise `build_graph_json` pour source/cible."
    if "exhaustive" in question_lower or "exhaustivite" in question_lower:
        return "Utilise `check_exhaustivite` pour l’état."

    # Requêtes simples
    if "heure" in question_lower:
        query = f"MATCH (t:Table {{nom_table: '{table}'}}) RETURN t.heure_lancement AS heure"
    elif "frequence" in question_lower:
        query = f"MATCH (t:Table {{nom_table: '{table}'}}) RETURN t.frequence_ingestion AS frequence"
    elif "suivi" in question_lower:
        query = f"MATCH (t:Table {{nom_table: '{table}'}}) RETURN t.suivie AS suivie"
    elif "description" in question_lower or "commentaire" in question_lower:
        query = f"MATCH (t:Table {{nom_table: '{table}'}}) RETURN t.commentaire AS commentaire"
    else:
        query = f"MATCH (t:Table {{nom_table: '{table}'}}) RETURN t"

    try:
        data = run_query(query)
        return str(data[0]) if data else f"Aucune donnée trouvée pour {table}."
    except Exception as e:
        return f"Erreur lors de la requête Neo4j : {e}"
