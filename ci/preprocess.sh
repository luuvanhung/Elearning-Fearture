#!/bin/bash

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
SRC_DIR=${ROOT_DIR}/src
cd ${ROOT_DIR}
echo ERP_PORT: ${ERP_PORT}

# Copy or download scret files
scp -i ${SSH_KEY} ${SERVER_SSH}:${CLIENT_SECRET_FILE} ${SRC_DIR}/api/credentials.json

# For docker
echo preprocess docker environment variables
cp -f ${ROOT_DIR}/ci/docker.env.template ${ROOT_DIR}/docker.env
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DJANGO_SETTINGS_MODULE=/DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_USER=/DB_USER=${DB_USER}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_PASSWORD=/DB_PASSWORD=${DB_PASSWORD}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_NAME=/DB_NAME=${DB_NAME}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_HOST=/DB_HOST=${DB_HOST}/g
find ${ROOT_DIR}/docker.env -type f -name "*" | xargs sed -i'' s/DB_PORT=/DB_PORT=${DB_PORT}/g

echo preprocess docker compose files
cp -f ${ROOT_DIR}/ci/docker-compose.yml.template ${ROOT_DIR}/docker-compose.yml
echo ${ROOT_DIR}/docker-compose.yml
find ${ROOT_DIR}/docker-compose.yml -type f -name "*" | xargs sed -i'' s%__DOCKER_IMAGE_NAME__%${DOCKER_REPOSITORY}:${DEPLOY_ENV}-latest%g
find ${ROOT_DIR}/docker-compose.yml -type f -name "*" | xargs sed -i'' s/__ERP_PORT__/${ERP_PORT}/g

echo preprocess docker file
cp -f ${ROOT_DIR}/ci/Dockerfile.template ${ROOT_DIR}/Dockerfile

# Backend config
echo preprocess config.env
cp -f ${SRC_DIR}/core/config.env.template ${SRC_DIR}/config.env
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SECRET_KEY=/SECRET_KEY=${SECRET_KEY}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_USER=/DB_USER=${DB_USER}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_PASSWORD=/DB_PASSWORD=${DB_PASSWORD}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_NAME=/DB_NAME=${DB_NAME}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_HOST=/DB_HOST=${DB_HOST}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DB_PORT=/DB_PORT=${DB_PORT}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/APP_NAME=/APP_NAME=${APP_NAME}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/API_HOST=/API_HOST=${API_HOST}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/CORS_ALLOW_ALL_ORIGINS=/CORS_ALLOW_ALL_ORIGINS=${CORS_ALLOW_ALL_ORIGINS}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%CORS_ALLOWED_ORIGINS=%CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEFAULT_CLIENT_ID=/DEFAULT_CLIENT_ID=${DEFAULT_CLIENT_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEFAULT_CLIENT_SECRET=/DEFAULT_CLIENT_SECRET=${DEFAULT_CLIENT_SECRET}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DJANGO_ALLOWED_HOSTS=/DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/USE_X_FORWARDED_HOST=/USE_X_FORWARDED_HOST=${USE_X_FORWARDED_HOST}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_CLIENT_ID=/SLACK_CLIENT_ID=${SLACK_CLIENT_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_CLIENT_SECRET=/SLACK_CLIENT_SECRET=${SLACK_CLIENT_SECRET}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_USER_OAUTH_TOKEN=/SLACK_USER_OAUTH_TOKEN=${SLACK_USER_OAUTH_TOKEN}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_BOT_USER_OAUTH_TOKEN=/SLACK_BOT_USER_OAUTH_TOKEN=${SLACK_BOT_USER_OAUTH_TOKEN}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_BOT_USER_ID=/SLACK_BOT_USER_ID=${SLACK_BOT_USER_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_DEFAULT_CHANNEL=/SLACK_DEFAULT_CHANNEL=${SLACK_DEFAULT_CHANNEL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_LEAVE_CHANNEL=/SLACK_LEAVE_CHANNEL=${SLACK_LEAVE_CHANNEL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SLACK_LUNCH_CHANNEL=/SLACK_LUNCH_CHANNEL=${SLACK_LUNCH_CHANNEL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEV_SLACK_USER_ID=/DEV_SLACK_USER_ID=${DEV_SLACK_USER_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEV_LINE_MANAGER_SLACK_USER_ID=/DEV_LINE_MANAGER_SLACK_USER_ID=${DEV_LINE_MANAGER_SLACK_USER_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST=/EMAIL_HOST=${EMAIL_HOST}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST_USER=\'\'/EMAIL_HOST_USER=\'${EMAIL_HOST_USER}\'/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_HOST_PASSWORD=\'\'/EMAIL_HOST_PASSWORD=\'${EMAIL_HOST_PASSWORD}\'/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%BLOCKED_EMAIL_DOMAINS=%BLOCKED_EMAIL_DOMAINS=${BLOCKED_EMAIL_DOMAINS}%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEFAULT_FROM_EMAIL=/DEFAULT_FROM_EMAIL=${DEFAULT_FROM_EMAIL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%WEB_INTERNAL=%WEB_INTERNAL=${WEB_INTERNAL}/%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEFAULT_EMAIL_ADMIN=/DEFAULT_EMAIL_ADMIN=${DEFAULT_EMAIL_ADMIN}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEV_MAIL=/DEV_MAIL=${DEV_MAIL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/CALENDAR_ID=/CALENDAR_ID=${CALENDAR_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/ALLOWED_SWAGGER=/ALLOWED_SWAGGER=${ALLOWED_SWAGGER}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_ACCESS_KEY_ID=/AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_SECRET_ACCESS_KEY=/AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/STORE_USER_FILES_ON_S3=/STORE_USER_FILES_ON_S3=${STORE_USER_FILES_ON_S3}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_STORAGE_BUCKET_NAME=/AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/AWS_S3_REGION_NAME=/AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/PRIVATE_KEY_FILE=/PRIVATE_KEY_FILE=${PRIVATE_KEY_FILE}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SUPER_ADMIN_EMAIL=/SUPER_ADMIN_EMAIL=${SUPER_ADMIN_EMAIL}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/SUPER_ADMIN_PASSWORD=/SUPER_ADMIN_PASSWORD=${SUPER_ADMIN_PASSWORD}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/DEBUG=/DEBUG=${DEBUG}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/WIT_TOKEN=/WIT_TOKEN=${WIT_TOKEN}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/INTENT_THRESHOLD=/INTENT_THRESHOLD=${INTENT_THRESHOLD}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%HRM_LEAVE_REQUEST_LINK=%HRM_LEAVE_REQUEST_LINK=${HRM_LEAVE_REQUEST_LINK}/%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%HRM_NEW_LEAVE_REQUEST_LINK=%HRM_NEW_LEAVE_REQUEST_LINK=${HRM_NEW_LEAVE_REQUEST_LINK}/%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%HRM_NEW_WFH_REQUEST_LINK=%HRM_NEW_WFH_REQUEST_LINK=${HRM_NEW_WFH_REQUEST_LINK}/%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s%HRM_APPROVAL_REQUEST_LINK=%HRM_APPROVAL_REQUEST_LINK=${HRM_APPROVAL_REQUEST_LINK}/%g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/USE_INVITE_ATTENDEES_GOOGLE=/USE_INVITE_ATTENDEES_GOOGLE=${USE_INVITE_ATTENDEES_GOOGLE}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/LIMIT_DOMAIN=/LIMIT_DOMAIN=${LIMIT_DOMAIN}/g
find ${SRC_DIR}/config.env -type f -name "*" | xargs sed -i'' s/EMAIL_DOMAIN=/EMAIL_DOMAIN=${EMAIL_DOMAIN}/g


# Front end
echo preprocess .env
cp -f ${SRC_DIR}/frontend/sample.env ${SRC_DIR}/frontend/.env
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s%VUE_APP_IMAGE_URL=%VUE_APP_IMAGE_URL=${IMAGE_URL}%g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s/VUE_APP_VALID_TIME=/VUE_APP_VALID_TIME=${VALID_TIME}/g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s%VUE_APP_BASE_URL=%VUE_APP_BASE_URL=${BASE_URL}%g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s%VUE_APP_API_URL=%VUE_APP_API_URL=${API_URL}%g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s/VUE_APP_END_MAIL=/VUE_APP_END_MAIL=${EMAIL_DOMAIN}/g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s%VUE_APP_BLOCKED_EMAIL_DOMAINS=%VUE_APP_BLOCKED_EMAIL_DOMAINS=${BLOCKED_EMAIL_DOMAINS}%g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s%VUE_APP_GOOGLE_CLIENT_ID=%VUE_APP_GOOGLE_CLIENT_ID=${VUE_APP_GOOGLE_CLIENT_ID}%g
find ${SRC_DIR}/frontend/.env -type f -name "*" | xargs sed -i'' s/VUE_APP_ALLOW_SEEKING_VIDEO=/VUE_APP_ALLOW_SEEKING_VIDEO=${ALLOW_SEEKING_VIDEO}/g

# Create file pub/pri KEY
cd $SRC_DIR
file="${SRC_DIR}/${PRIVATE_KEY_FILE}"
echo $file
if [ -f "$file" ]
then
	echo "File ${file}.key is already exists"
else
	openssl genrsa -out "${file}" 4096
	openssl rsa -in "${file}" -pubout > "${file}.pub"
	chmod 777 "${file}"
fi

echo "Done."
