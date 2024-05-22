# Default path config
PATH_CONFIG = '~/.aurora-cli/new_configuration.yaml'  # @todo

DEFAULT_CONFIG = """
## Application configuration file Aurora CLI
## Version config: 1.0.0

## The parameter sets the path to install psdk and search sdk
## Specify an existing directory
workdir: ~/Aurora

## Type output: short | command | verbose
output: short

## Path to sign keys
## name - The name you will see in the list
## key  - Path to the key.pem file
## cert - Path to the cert.pem file
keys:
  - name: Public
    key: ~/.aurora-cli/keys/regular_key.pem
    cert: ~/.aurora-cli/keys/regular_cert.pem

## Devices list
## host     - Device IP WI-FI or cable connection
## auth     - SSH password / SSH key path
## port     - SSH port
## devel-su - Device root password
devices:
  - host: 192.168.2.15
    auth: '00000'
    port: 22
    devel-su: '00000'
"""
