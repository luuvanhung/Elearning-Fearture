#!/bin/bash

# set -e
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 file-name" >&2
  exit 1
fi
PRIVATE_KEY_FILE=$1
ROOT_DIR=$(git rev-parse --show-toplevel)
SRC_DIR=${ROOT_DIR}/src

# Create file pub/pri KEY
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
