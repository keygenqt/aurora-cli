"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os
import stat
from pathlib import Path

import click

from aurora_cli.src.support.helper import find_path_file, prompt_index
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts
from aurora_cli.src.support.versions import get_versions_flutter

build_script = '''#!/bin/bash

###################################################
# Path to flutter
FLUTTER="$HOME/.local/opt/flutter-{tag}/bin/flutter"

# Build a version of your app.
# debug || profile || release
VERSION='release'

# The target platform for which the app is compiled.
# arm || arm64 || x64
PLATFORM='arm'

# Launch the installed application.
# true || false
RUN='false'
###################################################

# Open example folder if exist
if [ -d "example" ]; then
  cd example || exit
fi

# Start emulator
{{
  if [ "$PLATFORM" = "x64" ]; then
    aurora-cli emulator start
  fi
}} &> /dev/null

# Clear build
$FLUTTER clean

# Get dependency
$FLUTTER pub get

## Run build dart
$FLUTTER pub run build_runner build --delete-conflicting-outputs

{{
  # Change output
  exec 5>&1

  # Build aurora application
  output=$($FLUTTER build aurora --target-platform aurora-$PLATFORM --$VERSION | tee /dev/fd/5)

  # Get path to rmp
  listRPMs=$(echo "$output" | grep "│" | tr -d "\n" | sed 's/│//g' | sed 's/ //g' | sed 's/\.\//;/g')

  # Get package name
  for item in $(echo "$listRPMs" | tr ";" "\n")
  do
    if [ -n "$item" ] && [[ $item != *"-debug"* ]]; then
      package=$(basename "$item" | cut -d '-' -f1)
      break
    fi
  done

  # Error if package path empty
  if [[ -z $package ]]; then
    echo "Error find package name"
    exit 1;
  fi

  # Run sign and install
  for item in $(echo "$listRPMs" | tr ";" "\n")
  do
    if [ -n "$item" ]; then
      # Sign
      aurora-cli psdk sign -p "./$item"
      # Install
      if [[ "$PLATFORM" = "x64" ]]; then
        aurora-cli emulator install -p "./$item"
      else
        aurora-cli device install -p "./$item"
      fi
    fi
  done

  # Run package
  if [[ $RUN == "true" ]]; then
    for item in $(echo "$listRPMs" | tr ";" "\n")
    do
      if [ -n "$item" ] && [[ $item != *"-debug"* ]]; then
        if [[ "$PLATFORM" = "x64" ]]; then
          aurora-cli emulator run -p "$package" -v
        else
          aurora-cli device run -p "$package" -v
        fi
        break
      fi
    done
  fi

}} || {{
  echo 'Error build'
  exit 1;
}}
'''


@click.group(name='build', invoke_without_command=True)
@click.option('-l', '--latest', is_flag=True, help="Select latest version")
def group_flutter_build(latest: bool):
    """Add script to project for build Flutter application."""

    versions = get_versions_flutter()

    if not latest:
        echo_stdout(AppTexts.select_versions(versions))
        echo_stdout(AppTexts.array_indexes(versions), 2)

    # Query index
    index = prompt_index(versions, 1 if latest else None)

    # Select tag
    tag = versions[index]

    # Get path application
    application = Path(f'{os.getcwd()}/example')
    if not application.is_dir():
        application = Path(os.getcwd())

    # Find spec app flutter
    file_spec = find_path_file('spec', Path(f'{application}/aurora/rpm'))
    if not file_spec or not file_spec.is_file():
        if not click.confirm(AppTexts.flutter_project_not_found_confirm()):
            exit(0)

    # Get path to launch.json
    vscode_dir = Path(f'{os.getcwd()}/.vscode')
    vscode_dir.mkdir(parents=True, exist_ok=True)
    build_path = Path(f'{vscode_dir}/build.sh')

    if build_path.is_file():
        if not click.confirm(AppTexts.flutter_build_script_confirm()):
            exit(0)

    # Create .gdbinit app flutter
    with open(build_path, 'w') as file:
        print(build_script.format(tag=tag), file=file)

    # Add run permission
    os.chmod(build_path, os.stat(build_path).st_mode | stat.S_IEXEC)

    # Output
    echo_stdout(AppTexts.flutter_build_script_add_success(str(build_path)))
