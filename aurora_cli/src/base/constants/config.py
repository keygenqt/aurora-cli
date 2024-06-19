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

APP_FOLDER = '~/.aurora-cli'

# Default path config
CONFIG_PATH = f'{APP_FOLDER}/configuration3.yaml'

# Default config
CONFIG_DEFAULT = """## Application configuration file Aurora CLI
## Version config: 3.0.0

## The parameter sets the path to install psdk and search sdk
## Specify an existing directory
workdir: ~/

## Path to sign keys
## name - The name you will see in the list
## key  - Path to the key.pem file
## cert - Path to the cert.pem file
##
## Example:
## keys:
##   - name: Public
##     key: ~/.aurora-cli/regular_key.pem
##     cert: ~/.aurora-cli/regular_cert.pem
keys: []

## Devices list
## host     - Device IP WI-FI or cable connection
## auth     - SSH password / SSH key path
## port     - SSH port
## devel-su - Device root password
##
## Example:
## devices:
##   - host: 192.168.2.15
##     auth: '00000'
##     port: 22
##     devel-su: '00000'
devices:
  - host: 192.168.2.15
    auth: '00000'
    port: 22
    devel-su: '00000'
"""
