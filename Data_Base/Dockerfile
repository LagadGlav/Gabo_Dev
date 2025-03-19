# Utiliser l'image MySQL de base
FROM mysql:8.0

# Définir les variables d'environnement nécessaires
ENV MYSQL_ROOT_PASSWORD=Gabo
ENV MYSQL_DATABASE=Gabo_base

# Copier le script d'initialisation SQL dans le dossier spécial de MySQL
COPY ./init.sql /docker-entrypoint-initdb.d/
