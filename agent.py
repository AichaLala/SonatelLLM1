# agent.py
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import Ollama
from tool import ask_neo4j, build_graph_json, check_exhaustivite

llm = Ollama(model="mistral")

tools = [
    Tool(
        name="Métadonnées Hive",
        func=ask_neo4j,
        description="Donne des informations sur les métadonnées d'une table Hive (heure, fréquence, description, etc.)."
    ),
    Tool(
        name="Relations Source/Cible",
        func=build_graph_json,
        description="Renvoie les sources ou cibles d’une table Hive."
    ),
    Tool(
        name="Vérification Exhaustivité",
        func=check_exhaustivite,
        description="Vérifie si une table est exhaustive à partir de Neo4j."
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  #  pour voir ce que fait le LLM dans le terminal
)

def ask_agent(question: str) -> str:
    return agent.run(question)
