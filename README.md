# Aurora CLI 2.0

![picture](https://github.com/keygenqt/aurora-cli/blob/main/data/banner_small.png?raw=true)

[![PyPI version](https://badge.fury.io/py/aurora-cli.svg)](https://badge.fury.io/py/aurora-cli)

An application that simplifies the life of an application developer for the Aurora OS.

## Features

* sdk
    - available - Get available version Aurora SDK.
    - install - Download and run install Aurora SDK.
    - installed - Get version installed Aurora SDK.
* psdk
    - available - Get available version Aurora Platform SDK.
    - install - Download and install Aurora Platform SDK.
    - installed - Get installed list Aurora Platform SDK.
    - remove - Remove installed Aurora Platform SDK.
    - sudoers - Add sudoers permissions Aurora Platform SDK.
    - sign - Sign (with re-sign) RPM package.
    - validate - Validate RPM packages.
* flutter
    - available - Get available versions flutter.
    - install - Install Flutter SDK for Aurora OS.
    - installed - Get installed list Flutter SDK.
    - remove - Remove Flutter SDK.
* device
    - available - Get available devices from configuration.
    - command - Execute the command on the device.
    - upload - Upload file to ~/Download directory device.
    - install - Install RPM package on device.
    - run - Run package on device in container.
* emulator
    - available - Get available emulator.
    - start - Start emulator.
    - command - Execute the command on the emulator.
    - upload - Upload file to ~/Download directory emulator.
    - install - Install RPM package on emulator.
    - run - Run package on emulator in container.

## Usage

### Install dependencies

```shell
# Update
sudo apt update

# Install dependencies
sudo apt install python3-pip git git-lfs curl tar unzip bzip2
```

### Method 1

The standard way to distribute python packages.

```shell
python3 -m pip install aurora-cli
```

### Method 2

This method is as simple as possible - the entire application is in a pyz file.

```shell
# Create folder
mkdir ~/.local/opt

# Download
wget -x https://github.com/keygenqt/aurora-cli/raw/main/builds/aurora-cli-2.0.11.pyz \
  -O ~/.local/opt/aurora-cli.pyz

# Add alias to ~/.bashrc
alias aurora-cli='python3 ~/.local/opt/aurora-cli.pyz'

# Update environment
source ~/.bashrc
```

### Method 3

This method is suitable for development.

```shell
# Create folder
mkdir -p ~/.local/opt/aurora-cli

# Clone project
git clone https://github.com/keygenqt/aurora-cli.git ~/.local/opt/aurora-cli

# Open folder project
cd ~/.local/opt/aurora-cli

# Init environment
virtualenv .venv

# Open environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate environment
deactivate

# Add alias to ~/.bashrc
alias aurora-cli='cd ~/.local/opt/aurora-cli && .venv/bin/python -m aurora_cli'

# Update environment
source ~/.bashrc
```

### License

```
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
```
