# 🧠 Assistant Métadonnées (API FastAPI + Neo4j + Ollama)

Ce projet est une API FastAPI permettant d'interroger des métadonnées de tables Hive stockées dans Neo4j en langage naturel, grâce à un modèle de langage local (LLM Mistral via Ollama).

---

## 🚀 Fonctionnalités

- Obtenir la **source directe** ou la **lignée complète** d’une table
- Obtenir la **cible directe** d’une table
- Obtenir la **date de création** d’une table
- Obtenir le **propriétaire** d’une table
- Réponse automatique en langage naturel via **LLM Mistral (Ollama)** si la question n’est pas comprise

---

## 🛠️ Technologies utilisées

- **FastAPI** : Serveur web et endpoints REST
- **Neo4j** : Base de données de graphes pour stocker les relations entre tables
- **LangChain + Ollama (Mistral)** : Génération de réponses en langage naturel
- **HTML + JavaScript** : Interface simple de test local

---

## 📁 Structure du projet

```bash
api_LLM/
├── apillm.py             # Code principal de l’API FastAPI
├── requirements.txt      # Dépendances Python
├── index.html            # Interface locale web (facultative)
├── Documentation_Assistant_Metadata.docx  # Document de description complet
└── venv/                 # Environnement virtuel Python
