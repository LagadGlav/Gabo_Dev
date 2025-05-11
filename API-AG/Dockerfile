# Dockerfile-gunicorn
FROM python:3.9-slim

# Répertoire de l'application
WORKDIR /API-AG

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'intégralité du code de l'application dans le conteneur
COPY . /API-AG

# Gunicorn va écouter sur le port 8010
CMD ["gunicorn", "-w", "1", "--threads", "4", "-k", "gthread", "-b", "0.0.0.0:8020", "api-ag:app"]