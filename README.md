# Evaluation Python FastAPI

## Installation

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement virtuel sous Windows :

```bash
.venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

L'API est disponible sur :

http://127.0.0.1:8000

La documentation Swagger est disponible sur :

http://127.0.0.1:8000/docs
