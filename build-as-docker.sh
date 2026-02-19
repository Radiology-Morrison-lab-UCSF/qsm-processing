#!/bin/bash

set -e

dir_script="$(dirname "$(readlink -f "$0")")"/
cd "$dir_script"

# Build the Docker image for amd64 using your custom tag
docker build --platform=linux/amd64 . --tag ericcito1/qsmxt-plus:8.2.2

# Uncomment the next line if you later want to push to your DockerHub
# docker push ericcito1/qsmxt-plus:8.2.2