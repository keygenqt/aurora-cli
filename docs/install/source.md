# Install Aurora CLI from GitHub

This method is suitable for development.

### Create folder

```shell
mkdir -p ~/.local/opt/aurora-cli
```

### Clone project

```shell
git clone https://github.com/keygenqt/aurora-cli.git ~/.local/opt/aurora-cli
```

### Open folder project

```shell
cd ~/.local/opt/aurora-cli
```

### Init environment

```shell
virtualenv .venv
```

### Open environment

```shell
source .venv/bin/activate
```

### Install requirements

```shell
pip install -r requirements.txt
```

### Deactivate environment

```shell
deactivate
```

### Add alias to `~/.bashrc`

```shell
alias aurora-cli='_cli() { (cd ~/.local/opt/aurora-cli && .venv/bin/python -m aurora_cli "$@"); } && _cli'
```

### Update environment

```shell
source ~/.bashrc
```
