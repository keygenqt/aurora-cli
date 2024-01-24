# Sudoers chroot mer-sdk-chroot
import os
from pathlib import Path


# Get installed sdk
def get_sdk_installed():
    folders = [folder for folder in os.listdir(Path.home()) if
               os.path.isdir(Path.home() / folder) and 'Aurora' in folder and os.path.isfile(
                   Path.home() / folder / 'sdk-release')]
    if folders:
        with open(Path.home() / folders[0] / 'sdk-release') as f:
            return 'Aurora SDK: {}'.format(f.readline().strip().split('=')[1].replace('-base', ''))
    return None
