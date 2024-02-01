# Aurora CLI - Devices

### Available 

Get available devices from configuration.

**Example**

```shell
aurora-cli device available
```

### Command 

Execute the command on the device.

**Params**

* `--execute (-e)` - Command to execute on the device.
* `--index (-i)` - Device index from the config.

**Example**

```shell
aurora-cli device command -e 'ls'
```

### Upload 

Upload file to `~/Download` directory device.

**Params**

* `--path (-p)` - Path to file.
* `--index (-i)` - Device index from the config.

**Example**

```shell
aurora-cli device upload -p {path}
```

### Install 

Install RPM package on device.

**Params**

* `--path (-p)` - Path to RPM package.
* `--index (-i)` - Device index from the config.
* `--devel-su (-s)` - Password root, if empty using form config.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli device install -p {path}.rpm
```

### Run 

Run package on device in container.

**Params**

* `--package (-p)` - Package name app for run in container.
* `--index (-i)` - Device index from the config.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli device run -p {package name}
```
