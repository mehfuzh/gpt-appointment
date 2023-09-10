#!/bin/bash
# Gathers all requirements for the Docker file, builds it, and then pushes it to ECR.

set -eo pipefail

if [[ $1 && $2 ]]; then :
else
    printf '\nPlease supply an AWS profile, an AWS region, and an ECS repository.\n'
    printf '\n\tExample: bash docker_build_and_push.sh default us-west-2 anaplan-dev-ecr\n\n\n'
    exit
fi

readonly DOCKER_DIR="."
readonly ACR_REPOSITORY="$1"
readonly IMAGE_NAME="$2"

readonly DATE_STAMP=$(date +%Y%0m%0d-%0H%0M)

printf "\nLogging in to %s.\n" "$ACR_REPOSITORY"

# We want to execute the following command.
# shellcheck disable=SC2091
az acr login --name $ACR_REPOSITORY 

printf '\nBuilding Docker Image.\n'

COMPOSE_DOCKER_CLI_BUILD=1
DOCKER_BUILDKIT=1
DOCKER_DEFAULT_PLATFORM=linux/amd64

docker buildx  build --platform linux/amd64 -t "$IMAGE_NAME"  "$DOCKER_DIR/."


printf '\nTagging Docker image.\n'

docker tag "$IMAGE_NAME" "$ACR_REPOSITORY.azurecr.io/$IMAGE_NAME:latest"
docker tag "$IMAGE_NAME" "$ACR_REPOSITORY.azurecr.io/$IMAGE_NAME:$DATE_STAMP"

printf "\nPushing Docker image to %s.\n" "$ECR_REPOSITORY"

docker push "$ACR_REPOSITORY.azurecr.io/$IMAGE_NAME:$DATE_STAMP"
docker push "$ACR_REPOSITORY.azurecr.io/$IMAGE_NAME:latest"

printf "\nDocker iamges in %s.\n" "$IMAGE_NAME"

az acr repository list --name "$ACR_REPOSITORY.azurecr.io" --output table


printf "\nCreated and pushed a new Docker image to %s.\n\n" "$ACR_REPOSITORY"
