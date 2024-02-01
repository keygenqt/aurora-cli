# Aurora CLI - Configuration

When you first launch the application, you will be prompted to create a configuration file. 
You can find it along the path: `~/.aurora-cli/configuration.yaml`. 
You can adjust it to suit yourself by adding keys or devices.

It is described in sufficient detail, I present it here:

```yaml
## Application configuration file Aurora CLI
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
```

!!! info
    
    The application will also offer you to download public keys.
