# Install Aurora CLI *.pyz

This method is as simple as possible - the entire application is in a pyz file.

### Create folder

```shell
mkdir ~/.local/opt
```

### Download

```shell
wget -x https://github.com/keygenqt/aurora-cli/raw/main/builds/aurora-cli-2.4.4.pyz \
  -O ~/.local/opt/aurora-cli.pyz
```

### Add alias to `~/.bashrc`

```shell
alias aurora-cli='python3 ~/.local/opt/aurora-cli.pyz'
```

### Update environment

```shell
source ~/.bashrc
```
