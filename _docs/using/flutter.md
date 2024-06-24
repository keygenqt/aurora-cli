# Aurora CLI - Flutter for Aurora OS

### Available

Get available versions flutter.

**Example**

```shell
aurora-cli flutter available
```

### Install

Install Flutter SDK for Aurora OS.

**Params**

* `--latest (-l)` - Aurora select latest version for install.

**Example**

```shell
aurora-cli flutter install --latest
```

### Installed

Get installed list Flutter SDK.

**Example**

```shell
aurora-cli flutter installed
```

### Remove

Remove Flutter SDK.

**Example**

```shell
aurora-cli flutter remove
```

### Build

Add script to project for build Flutter application.

**Params**

* `--index (-i)` - Specify index version.
* `--apm (-a)` - Use new install APM.
* `--yes (-y)` - All yes confirm.

**Example**

```shell
aurora-cli flutter build
```

### Debug gdb

Project configure and run for gdb debug.

**Params**

* `--index (-i)` - Specify index device.
* `--port (-p)` - Specify port for gdb server.
* `--emulator (-e)` - Run on emulator.
* `--verbose (-v)` - Command output.

**Example**

```shell
aurora-cli flutter debug gdb
```

### Debug dart

Project configure and run on device for dart debug or hot reload.

**Params**

* `--index (-i)` - Specify index device.
* `--emulator (-e)` - Run on emulator.
* `--yes (-y)` - All yes confirm.
* `--verbose (-v)` - Command output.

**Example**

```shell
aurora-cli flutter debug dart
```

### Plugins

Get types plugins info. Run in folder with pubspec.yaml.

**Example**

```shell
aurora-cli flutter plugins
```

### Icons

Create icons size for flutter project.

**Params**

* `--path (-p)` - Path to image.

**Example**

```shell
aurora-cli flutter icons -p {/path/to/file.png}
```

### Format project Dart & C++

Formatting C++ and Dart code in a Flutter project according to the
[rules](https://omprussia.gitlab.io/flutter/flutter/faq/#dart) adopted in Flutter for Aurora OS.
Call it in the project package or specify the path to it.

**Params**

* `--path (-p)` - Path to project.
* `--verbose (-v)` - Command output.

**Example**

```shell
aurora-cli flutter format
```
