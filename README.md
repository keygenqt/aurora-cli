# Aurora CLI

![picture](https://github.com/keygenqt/aurora-cli/blob/main/data/banner_small.png?raw=true)

[![PyPI version](https://badge.fury.io/py/aurora-cli.svg)](https://badge.fury.io/py/aurora-cli)

An application that simplifies the life of an application developer for the Aurora OS.

## Features

* sdk
    - available - Get available version Aurora SDK.
    - install - Download and run install Aurora SDK.
    - installed - Get version installed Aurora SDK.
    - tool - Run maintenance tool (remove, update).
* psdk
    - available - Get available version Aurora Platform SDK.
    - install - Download and install Aurora Platform SDK.
    - installed - Get installed list Aurora Platform SDK.
    - remove - Remove installed Aurora Platform SDK.
    - sudoers - Add/Del sudoers permissions Aurora Platform SDK.
    - sign - Sign (with re-sign) RPM package.
    - validate - Validate RPM packages.
    - sdk-install - Install RPM packages to target.
    - sdk-remove - Remove package from target.
    - list-targets - Get list targets Aurora Platform SDK.
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

## Install dependencies

```shell
# Update
sudo apt update

# Install dependencies
sudo apt install python3-pip git git-lfs curl tar unzip bzip2
```

## Install app

```shell
python3 -m pip install aurora-cli
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
