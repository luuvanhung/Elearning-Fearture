#!/bin/bash

# set e

SERVER_SSH=$1
DEPLOY_PATH=$2
SSH_KEY=$3
AWS_CONFIG=$4
DOCKER_REPOSITORY=$5
DEPLOY_ENV=$6
API_CLUSTER=$7
API_SERVICE_NAME=$8


ROOT_DIR=$(git rev-parse --show-toplevel)
DOCKER_IMAGE_REVISION=revision-$(git show --format="%H" --no-patch)
echo DOCKER_REPOSITORY: $DOCKER_REPOSITORY
echo DOCKER_IMAGE_NAME: $DOCKER_IMAGE_NAME

cd ${ROOT_DIR}

#syn source to deploy server
echo syn source to server
rsync -e "ssh -i  ${SSH_KEY}" -avzh --delete-after --omit-dir-times --exclude '.git' ./  ${SERVER_SSH}:${DEPLOY_PATH}

#build and run docker container
echo building source...
ssh -i ${SSH_KEY} ${SERVER_SSH} env DEPLOY_PATH="$DEPLOY_PATH" AWS_CONFIG="$AWS_CONFIG" DOCKER_REPOSITORY="$DOCKER_REPOSITORY" DEPLOY_ENV="$DEPLOY_ENV" DOCKER_IMAGE_REVISION="$DOCKER_IMAGE_REVISION" API_CLUSTER="$API_CLUSTER" API_SERVICE_NAME="$API_SERVICE_NAME"  /bin/bash <<'EOT'
cd ${DEPLOY_PATH}
echo login ecr
docker run --rm -t -v ${AWS_CONFIG}:/root/.aws -v $(pwd):/aws amazon/aws-cli ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $DOCKER_REPOSITORY || exit 1\

echo build and push image to ecr
docker build -t ${DOCKER_REPOSITORY}:${DEPLOY_ENV}-${DOCKER_IMAGE_REVISION} . || exit 1\
docker push ${DOCKER_REPOSITORY}:${DEPLOY_ENV}-${DOCKER_IMAGE_REVISION} || exit 1\
echo update latest tag
docker tag ${DOCKER_REPOSITORY}:${DEPLOY_ENV}-${DOCKER_IMAGE_REVISION} ${DOCKER_REPOSITORY}:${DEPLOY_ENV}-latest
docker push ${DOCKER_REPOSITORY}:${DEPLOY_ENV}-latest || exit 1\

echo migate database
docker run --rm -v ${AWS_CONFIG}:/root/.aws -v $(pwd):/aws amazon/aws-cli ecs run-task --cli-input-json file:///aws/db-migration-task.json || exit 1\
echo update service
docker run --rm -v ${AWS_CONFIG}:/root/.aws -v $(pwd):/aws amazon/aws-cli ecs update-service --cluster ${API_CLUSTER} --service ${API_SERVICE_NAME} --force-new-deployment || exit 1\
EOT
