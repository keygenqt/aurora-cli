#!/bin/bash

########################
## Build pyz application
########################

# Upgrade
python3 -m pip install --upgrade shiv

APP_NAME=$(grep "APP_NAME = '" aurora_cli/src/support/conf.py  | sed "s/ //g" | sed "s/'//g" | sed "s/APP_NAME=//g")
APP_VERSION=$(grep "APP_VERSION = '" aurora_cli/src/support/conf.py  | sed "s/ //g" | sed "s/'//g" | sed "s/APP_VERSION=//g")

# Clean old build
rm -r dist build ./*.egg-info

# Dependency
pip install . --target dist

# Create dir builds if not exist
mkdir -pv builds

# Build pyz
shiv --site-packages dist --compressed -p '.venv python' -o "builds/$APP_NAME-$APP_VERSION.pyz" -e aurora_cli.__main__:main

# Clean after build
rm -r dist build ./*.egg-info
