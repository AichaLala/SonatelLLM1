2. ✅ Prérequis
🐍 Python 3.10+
python --version
📦 Installer les dépendances
pip install -r requirements.txt
🌐 Neo4j local
Installer Neo4j Desktop : https://neo4j.com/download/

Créer une base locale avec :
URI : bolt://localhost:7687
Username : neo4j
Password : Sonatel2025

🧠 Modèle LLM (Mistral via Ollama)
Installer Ollama : https://ollama.com/download
Lancer le modèle :
ollama run mistral
⚠️ Obligatoire : le modèle Mistral doit être actif en fond sinon l’API ne pourra pas répondre.


▶️ Lancer l’API
uvicorn heart:app --reload
Accès API : http://localhost:8000
Docs Swagger : http://localhost:8000/docs

📮 Utilisation dans Postman
Requête POST
POST http://localhost:8000/ask
Header:
COntent-Type:application/json
Exemple de corps JSON

{
  "question": "Quelle est la source de la table cdrnm ?"
}

💡 Exemples de questions
Quelle est la source de la table cdrnm ?

Quelle est la cible de trusted_report_bundle_offer ?

Quelle est la fréquence d’ingestion de client_kpi ?

La table sargal est-elle suivie ?

La table transactions est-elle exhaustive ?

⚠️ Pour l’exhaustivité, l’API ajoute automatiquement le préfixe trusted_ au nom de la table.