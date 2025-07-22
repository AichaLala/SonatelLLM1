# heart.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import ask_agent
from tool import check_exhaustivite, build_graph_json, ask_neo4j

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: AskRequest):
    question = request.question.lower()

    if "source" in question or "cible" in question:
        return {"graph": build_graph_json(question)}

    if "exhaustive" in question or "exhaustivite" in question:
        return {"graph": check_exhaustivite(question)}

    # Métadonnées simples
    metadata = ask_neo4j(question)
    return {"response": metadata}
