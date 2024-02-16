# Aurora CLI - Emulator

### Start 

Start emulator.

**Params**

* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli emulator start
```

### Screenshot

Take screenshot emulator.

**Params**

* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli emulator screenshot
```

### Recording

Recording video from emulator.

**Params**

* `--convert (-c)` - Convert video to mp4.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli emulator recording
```

### Command 

Execute the command on the emulator.

**Params**

* `--execute (-e)` - Command to execute on the emulator.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli emulator command -e 'ls'
```

### Run 

Run package on emulator in container.

**Params**

* `--package (-p)` - Package name app for run in container.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli device run -p {package name}
```

### Install 

Install RPM package on emulator.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli emulator install -p {path}.rpm
```

### Upload 

Upload file to `~/Download` directory emulator.

**Params**

* `--path (-p)` - Path to file.

**Example**

```shell
aurora-cli emulator upload -p {path}
```




