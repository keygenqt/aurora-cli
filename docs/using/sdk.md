# Aurora CLI - Aurora SDK

### Available 

Get available version Aurora SDK.

**Params**

* `--show-all (-a)` - Show all versions.

**Example**

```shell
aurora-cli sdk available
```

### Install 

Download and run install Aurora SDK.

**Params**

* `--show-all (-a)` - Show all versions.
* `--latest (-l)` - Aurora select latest version for install.
* `--install-type (-t)` - Download installer `offline` or `online` (default - `online`).

**Example**

```shell
aurora-cli sdk install --latest
```

### Installed 

Get version installed Aurora SDK.

**Example**

```shell
aurora-cli sdk installed
```

### Tool 

Run maintenance tool (remove, update).

**Example**

```shell
aurora-cli sdk tool
```
