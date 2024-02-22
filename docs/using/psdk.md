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

### List targets 

Get list targets.

**Example**

```shell
aurora-cli psdk list-targets
```

### Sign 

Sign (with re-sign) RPM package.

**Params**

* `--path (-p)` - Path to RPM package.
* `--index (-i)` - Keys index from the config.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk sign -p {path}
```

### Validate 

Validate RPM packages.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk validate -p {path}
```

### Package install 

Install RPM packages to target.

**Params**

* `--path (-p)` - Path to RPM package.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk package-install -p {path}
```

### Package remove 

Remove RPM packages from target.

**Params**

* `--package (-p)` - Package name.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk package-remove -p {package.name}
```

### Package search 

Search installed RPM packages in target.

**Params**

* `--package (-p)` - Package name.
* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk package-search -p {package.name}
```

### Clear

Remove snapshots targets.

**Params**

* `--verbose (-v)` - Detailed output.

**Example**

```shell
aurora-cli psdk clear
```
