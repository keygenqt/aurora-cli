# Aurora CLI - Emulator

### Start 

Start emulator.

**Example**

```shell
aurora-cli emulator start
```

### Available 

Get available emulator from configuration.

**Example**

```shell
aurora-cli emulator available
```

### Command 

Execute the command on the emulator.

**Params**

* `--execute (-e)` - Command to execute on the emulator.

**Example**

```shell
aurora-cli emulator command -e 'ls'
```

### Upload 

Upload file to `~/Download` directory emulator.

**Params**

* `--path (-p)` - Path to file.

**Example**

```shell
aurora-cli emulator upload -p {path}
```

### Install 

Install RPM package on emulator.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli emulator install -p {path}.rpm
```

### Run 

Run package on emulator in container.

**Params**

* `--package (-p)` - Package name app for run in container.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli device run -p {package name}
```
