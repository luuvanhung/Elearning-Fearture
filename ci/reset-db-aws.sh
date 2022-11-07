#!/bin/bash

# set e

SERVER_SSH=$1
DEPLOY_PATH=$2
SSH_KEY=$3
AWS_CONFIG=$4


ROOT_DIR=$(git rev-parse --show-toplevel)
cd ${ROOT_DIR}

#syn source to deploy server
echo syn source to server
rsync -e "ssh -i  ${SSH_KEY}" -avzh --delete-after --omit-dir-times --exclude '.git' ./  ${SERVER_SSH}:${DEPLOY_PATH}

ssh -i ${SSH_KEY} ${SERVER_SSH} env DEPLOY_PATH="$DEPLOY_PATH" AWS_CONFIG="$AWS_CONFIG" /bin/bash <<'EOT'
cd ${DEPLOY_PATH}
echo reset database
docker run --rm -v ${AWS_CONFIG}:/root/.aws -v $(pwd):/aws amazon/aws-cli ecs run-task --cli-input-json file:///aws/db-reset-task.json || exit 1\
EOT
