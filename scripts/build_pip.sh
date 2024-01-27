#!/bin/bash

########################
## Build pip application
########################

# Clean old build
rm -r dist ./*.egg-info

# Upgrade
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine

# Build
python3 -m build

# Clean after build
rm -r ./*.egg-info

# Upload
# python3 -m twine upload --repository testpypi dist/*
# python3 -m twine upload dist/*


