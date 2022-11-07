#!/bin/bash

set -e

ROOT_DIR=$(git rev-parse --show-toplevel)
cd ${ROOT_DIR}
# Migration task
echo preprocess database migration task
cp -f ${ROOT_DIR}/ci/db-migration-task.json.template ${ROOT_DIR}/db-migration-task.json
find ${ROOT_DIR}/db-migration-task.json -type f -name "*" | xargs sed -i'' s,__API_CLUSTER__,${API_CLUSTER},g
find ${ROOT_DIR}/db-migration-task.json -type f -name "*" | xargs sed -i'' s,__API_SUBNET__,${API_SUBNET},g
find ${ROOT_DIR}/db-migration-task.json -type f -name "*" | xargs sed -i'' s,__API_SECURIRY_GROUP__,${API_SECURIRY_GROUP},g
find ${ROOT_DIR}/db-migration-task.json -type f -name "*" | xargs sed -i'' s,__DB_MIGRATION_TASK_DEFINITION__,${DB_MIGRATION_TASK_DEFINITION},g

echo preprocess database reset task
cp -f ${ROOT_DIR}/ci/db-reset-task.json.template ${ROOT_DIR}/db-reset-task.json
find ${ROOT_DIR}/db-reset-task.json -type f -name "*" | xargs sed -i'' s,__API_CLUSTER__,${API_CLUSTER},g
find ${ROOT_DIR}/db-reset-task.json -type f -name "*" | xargs sed -i'' s,__API_SUBNET__,${API_SUBNET},g
find ${ROOT_DIR}/db-reset-task.json -type f -name "*" | xargs sed -i'' s,__API_SECURIRY_GROUP__,${API_SECURIRY_GROUP},g
find ${ROOT_DIR}/db-reset-task.json -type f -name "*" | xargs sed -i'' s,__DB_RESET_TASK_DEFINITION__,${DB_RESET_TASK_DEFINITION},g

echo "Preprocess done."
