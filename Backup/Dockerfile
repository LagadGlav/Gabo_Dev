FROM python:3.9-slim


RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt/lists/*

WORKDIR /Backup

# Copier le fichier requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script
COPY backup.py ./backup.py

# Point d'entrée pour exécuter le script au démarrage
CMD ["python", "backup.py"]
