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


def get_app_name():
    return 'aurora-cli'


def get_app_version():
    return '2.0.11'


def get_default_config():
    return """## Application configuration file Aurora CLI 2.0
## Version config: 0.0.1

## Path to sign keys
## name - The name you will see in the list
## key  - Path to the key.pem file
## cert - Path to the cert.pem file
keys:
  - name: Public
    key: ~/.aurora-cli/keys/regular_key.pem
    cert: ~/.aurora-cli/keys/regular_cert.pem

## Devices list
## ip       - Device IP WI-FI or cable connection
## pass     - SSH password
## port     - SSH port
## devel-su - Device root password
devices:
  - ip: 192.168.2.15
    pass: '00000'
    port: 22
    devel-su: '00000'
"""
