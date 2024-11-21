#!/bin/bash

######################
## Example validate CI
######################

# Path to package RPM
rpm=$1

## Validate profile.
# regular - default for all
profile='regular'
## Get arch from rpm name.
# It is enough to check one architecture, most likely they will match (но это не точно).
arch=$(echo $rpm | rev | cut -d '.' -f 2 | rev)
## Get first installed psdk.
# We need to understand which psdk we will be accessing.
version=$(aurora-cli api --route='/psdk/installed' | grep '"5.' | head -n 1 | xargs | sed 's/,//g')
## Get target by arch
# We can get the target name from the package name architecture.
target=$(aurora-cli api --route="/psdk/targets?version=$version" | grep -E "\"AuroraOS.+$arch" | head -n 1 | xargs | sed 's/,//g')

# Validate
code=$(aurora-cli api --route="/psdk/package/validate?version=$version&target=$target&path=$rpm&profile=$profile" | grep "code" | head -n 1 | xargs | sed 's/,//g' | sed 's/code: //g')
if [ "$code" == "200" ]; then
  echo 'Validate success!'
  exit 0;
else
  echo 'Validate error!'
  exit 1;
fi
