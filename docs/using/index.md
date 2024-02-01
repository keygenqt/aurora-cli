# Using Aurora CLI

The application allows you to simplify routine work with the Aurora OS toolchain, 
simplify lengthy commands and combine disparate Linux functionality in one simple application.

For example, you want to validate a package:

1. You need to get the name of the target.
2. You need to enter the command.

This is what we roughly get in the standard version:

```shell
aurora_psdk sb2 -t "AuroraOS-5.0.0.60-base-aarch64" -m emulate rpm-validator {path}
```

Or an option with Aurora CLI:

```shell
aurora-cli psdk validate -p {path}
```

And your target will be specified by the application.
This includes installing the package on the device and the emulator, and installing: Platfrom SDK, Aurora SDK Flutter SDK, package signing and much more.

It's easier with Aurora CLI!
