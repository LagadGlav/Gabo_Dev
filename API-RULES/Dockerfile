FROM python:3.9-slim

WORKDIR /API-RULES

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script
COPY api_rules.py ./api_rules.py

# Point d'entrée pour exécuter le script au démarrage
# Gunicorn va écouter sur le port 8010
CMD ["gunicorn", "-w", "1", "--threads", "1", "-k", "gthread", "-b", "0.0.0.0:8030", "api_rules:app"]
