# Install Aurora CLI *.pyz

This method is as simple as possible - the entire application is in a pyz file.

```shell
# Create folder
mkdir ~/.local/opt

# Download
wget -x https://github.com/keygenqt/aurora-cli/raw/main/builds/aurora-cli-2.1.0.pyz \
  -O ~/.local/opt/aurora-cli.pyz

# Add alias to ~/.bashrc
alias aurora-cli='python3 ~/.local/opt/aurora-cli.pyz'

# Update environment
source ~/.bashrc
```
