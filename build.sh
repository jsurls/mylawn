#!/bin/bash

SETTINGS_DIR=$1
if [ ! -d "$SETTINGS_DIR" ]; then
  echo "Missing settings dir!"
  exit 1
fi

APP_NAME=mylawn
APP_DIR=${APP_NAME}
BUILD_DIR=build

## Clean
rm -fr ${BUILD_DIR}
rm -f ${APP_NAME}.zip

## Source
source venv/bin/activate

## Pull down dependencies
pip install -t "${BUILD_DIR}" -r requirements.txt

## Remove dependency dist-info dirs
rm -fr ${BUILD_DIR}/*dist-info

## Add project
cp -r ${APP_DIR}/* ${BUILD_DIR}

## Add config
cp -r ${SETTINGS_DIR} ${BUILD_DIR}

## Zip project
cd ${BUILD_DIR}
zip -r ${APP_NAME}.zip * --exclude \*.pyc
mv ${APP_NAME}.zip ..
