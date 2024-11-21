#!/bin/bash

##################################
## Example install app to emulator
##################################

# Package RPM id (example: ru.auroraos.RSSReader)
package=$1

# Run emulator
aurora-cli api --route="/emulator/start" &> /dev/null
# Get first installed psdk.
version=$(aurora-cli api --route='/psdk/installed' | grep '"5.' | head -n 1 | xargs | sed 's/,//g')

# Download rpm package
path=$(aurora-cli api --route="/apps/download?app_id=$package&arch=x86_64" | grep '"value": "/' | head -n 1 | sed 's/"value": //g' | xargs)
# Sign rpm package
aurora-cli api --route="/psdk/package/sign?path=$path&version=$version" &> /dev/null
# Install package
code=$(aurora-cli api --route="/emulator/package/install?path=$path&apm=true&reinstall=true" | grep "code" | tail -n 1 | xargs | sed 's/,//g' | sed 's/code: //g')
if [ "$code" == "200" ]; then
  echo 'Installation successful!'
  exit 0;
else
  echo 'Installation error!'
  exit 1;
fi

