# agent.py
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import Ollama
from tool import ask_neo4j

# ✅ Initialisation du modèle
llm = Ollama(model="mistral")

# ✅ Création de l'outil connecté à Neo4j
tool = Tool(
    name="tool",
    func=ask_neo4j,
    description="Répond aux questions sur les métadonnées des tables Hive à partir de Neo4j"
)

# ✅ Création de l'agent
agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# ✅ Fonction appelée dans app.py
def ask_agent(question: str) -> str:
    return agent.run(question)
