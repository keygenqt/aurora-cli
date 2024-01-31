# Install Aurora CLI from GitHub

This method is suitable for development.

```shell
# Create folder
mkdir -p ~/.local/opt/aurora-cli

# Clone project
git clone https://github.com/keygenqt/aurora-cli.git ~/.local/opt/aurora-cli

# Open folder project
cd ~/.local/opt/aurora-cli

# Init environment
virtualenv .venv

# Open environment
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Deactivate environment
deactivate

# Add alias to ~/.bashrc
alias aurora-cli='_cli() { (cd ~/.local/opt/aurora-cli && .venv/bin/python -m aurora_cli "$@"); } && _cli'

# Update environment
source ~/.bashrc
```
