#!/bin/bash

########################
## Build pyz application
########################

APP_NAME=$(grep name setup.py | sed "s/ //g" | sed "s/',//g" | sed "s/name='//g")
APP_VERSION=$(grep version setup.py | sed "s/ //g" | sed "s/',//g" | sed "s/version='//g")

# Clean old build
rm -r dist build ./*.egg-info

# Dependency
pip install . --target dist

# Build pyz
shiv --site-packages dist --compressed -p '.venv python' -o "builds/$APP_NAME-$APP_VERSION.pyz" -e aurora_cli.__main__:main

# Clean after build
rm -r dist build ./*.egg-info
