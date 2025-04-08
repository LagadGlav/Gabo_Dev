# Dockerfile-gunicorn
FROM python:3.9-slim

# Répertoire de l'application
WORKDIR /API-AP

# Copier le fichier requirements (ajoutez-y toutes vos dépendances, y compris gunicorn)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'intégralité du code de l'application dans le conteneur
COPY . /API-AP

# Gunicorn va écouter sur le port 8010
CMD ["gunicorn", "-w", "1", "--threads", "4", "-k", "gthread", "-b", "0.0.0.0:8010", "api-ap:app"]