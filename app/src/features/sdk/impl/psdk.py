# Sudoers chroot mer-sdk-chroot
import os
import subprocess
from pathlib import Path

from cffi.backend_ctypes import unicode

MER_SDK_CHROOT = '/etc/sudoers.d/mer-sdk-chroot'
MER_SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {path_chroot}/mer-sdk-chroot
Defaults!{path_chroot}/mer-sdk-chroot env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''

# Sudoers chroot sdk-chroot
SDK_CHROOT = '/etc/sudoers.d/sdk-chroot'
SDK_CHROOT_DATA = '''{username} ALL=(ALL) NOPASSWD: {path_chroot}/sdk-chroot
Defaults!{path_chroot}/sdk-chroot env_keep += "SSH_AGENT_PID SSH_AUTH_SOCK"
'''


# Get list installed psdk
def get_list_psdk_installed():
    results = {}
    folders = [folder for folder in os.listdir(Path.home()) if
               os.path.isdir(Path.home() / folder) and 'Platform' in folder and os.path.isfile(
                   Path.home() / folder / 'sdks' / 'aurora_psdk' / 'sdk-chroot')]
    for folder in folders:
        results[folder] = str(Path.home() / folder / 'sdks' / 'aurora_psdk' / 'sdk-chroot')
    return results


# Check is add psdk sudoers and run sudo query
def check_sudoers_chroot(psdk_key):
    if os.path.isfile(MER_SDK_CHROOT):
        with open(MER_SDK_CHROOT) as f:
            if psdk_key in f.read():
                return

    subprocess.call(['sudo', 'echo', '-n'])


# Get list psdk targets
def get_list_targets(chroot):
    targets = []
    with subprocess.Popen([
        chroot,
        'sdk-assistant',
        'list',
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        for line in iter(lambda: process.stdout.readline(), ""):
            if not line:
                break
            line = unicode(line.rstrip(), "utf-8")
            if '─' in line and 'default' not in line:
                targets.append(line[2:])

    return targets
