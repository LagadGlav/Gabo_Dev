#!/bin/bash

# Nom d'utilisateur Docker Hub
DOCKER_USER="lagadglav"

# Se connecter à Docker Hub
docker login -u "$DOCKER_USER"

# Build and push images
docker build -t "$DOCKER_USER/gabo-compose-app:latest" ./APP
docker push "$DOCKER_USER/gabo-compose-app:latest"

docker build -t "$DOCKER_USER/gabo-compose-api-add_game:latest" ./APP-AG
docker push "$DOCKER_USER/gabo-compose-api-add_game:latest"

docker build -t "$DOCKER_USER/gabo-compose-api-add_player:latest" ./APP-AP
docker push "$DOCKER_USER/gabo-compose-api-add_player:latest"

docker build -t "$DOCKER_USER/gabo-compose-nginx:latest" ./nginx
docker push "$DOCKER_USER/gabo-compose-nginx:latest"

docker build -t "$DOCKER_USER/gabo-compose-database:latest" ./Data_Base
docker push "$DOCKER_USER/gabo-compose-database:latest"

docker build -t "$DOCKER_USER/gabo-compose-backup:latest" ./Backup
docker push "$DOCKER_USER/gabo-compose-backup:latest"

