FROM python:3.9-slim


RUN apt-get update && apt-get install -y mariadb-client && rm -rf /var/lib/apt/lists/*

WORKDIR /Backup

# Installer les dépendances
RUN pip install requests

# Copier le script
COPY backup.py ./backup.py

# Point d'entrée pour exécuter le script au démarrage
CMD ["python", "backup.py"]
