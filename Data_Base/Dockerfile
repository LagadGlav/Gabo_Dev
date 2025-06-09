# Utiliser l'image MySQL de base
FROM mysql:8.0

# Copier le script d'initialisation SQL dans le dossier spécial de MySQL
COPY ./init.sql /docker-entrypoint-initdb.d/
