#!/bin/bash

##########################
## Example check-format CI
##########################

# Path to folder with flutter project
project=$1

## Get first installed flutter.
# We need to understand which flutter we will be accessing.
version=$(aurora-cli api --route='/flutter/installed' | grep -E "\"[0-9].+" | head -n 1 | xargs | sed 's/,//g')

# Check format
code=$(aurora-cli api --route="/flutter/project/check-format?path=$project&version=$version" | grep "code" | head -n 1 | xargs | sed 's/,//g' | sed 's/code: //g')
if [ "$code" == "200" ]; then
  echo 'There is formatting!'
  exit 0;
else
  echo 'No formatting!'
  exit 1;
fi
