#!/bin/bash

# Nom d'utilisateur Docker Hub
DOCKER_USER="lagadglav"

# Se connecter à Docker Hub
docker login -u "$DOCKER_USER"

# Build and push images
docker build -t "$DOCKER_USER/gabo-app:latest" ./APP
docker push "$DOCKER_USER/gabo-app:latest"

docker build -t "$DOCKER_USER/gabo-api-add_game:latest" ./API-AG
docker push "$DOCKER_USER/gabo-api-add_game:latest"

docker build -t "$DOCKER_USER/gabo-api-add_player:latest" ./API-AP
docker push "$DOCKER_USER/gabo-api-add_player:latest"


docker build -t "$DOCKER_USER/gabo-nginx:latest" ./nginx
docker push "$DOCKER_USER/gabo-nginx:latest"

docker build -t "$DOCKER_USER/gabo-database:latest" ./Data_Base
docker push "$DOCKER_USER/gabo-database:latest"

docker build -t "$DOCKER_USER/gabo-backup:latest" ./Backup
docker push "$DOCKER_USER/gabo-backup:latest"

