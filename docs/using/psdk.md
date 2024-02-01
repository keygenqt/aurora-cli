# Aurora CLI - Aurora Platform SDK

### Available 

Get available version Aurora Platform SDK.

**Example**

```shell
aurora-cli psdk available
```

### Install 

Download and install Aurora Platform SDK.

**Params**

* `--latest (-l)` - Aurora select latest version for install.

**Example**

```shell
aurora-cli psdk install --latest
```

### Installed 

Get installed list Aurora Platform SDK.

**Example**

```shell
aurora-cli psdk installed
```

### Remove 

Remove installed Aurora Platform SDK.

**Example**

```shell
aurora-cli psdk remove
```

### Sudoers 

Add/Del sudoers permissions Aurora Platform SDK.

**Params**

* `--delete (-d)` - For delete sudoers permissions.

**Example**

```shell
aurora-cli psdk sudoers
```

### Sign 

Sign (with re-sign) RPM package.

**Params**

* `--path (-p)` - Path to RPM package.
* `--index (-i)` - Keys index from the config.
* `--key-path (-k)` - You can specify the path to the key, by default it is taken from the config.
* `--cert-path (-c)` - You can specify the path to the cert, by default it is taken from the config.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli psdk sign -p {path}
```

### Validate 

Validate RPM packages.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli psdk validate -p {path}
```

### SDK install

Install RPM packages to target.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli psdk sdk-install -p {path}
```

### SDK remove

Remove package from target.

**Params**

* `--package (-p)` - Package name.
* `--verbose (-v)` - Detailed log output.

**Example**

```shell
aurora-cli psdk sdk-remove -p {package name}
```

### List targets

Get list targets Aurora Platform SDK.

**Example**

```shell
aurora-cli psdk list-targets
```

