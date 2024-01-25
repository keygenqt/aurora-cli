import subprocess

from cffi.backend_ctypes import unicode


# Get emulator Aurora SDK virtualbox
def get_emulator_vm():
    output, error = subprocess.Popen([
        'VBoxManage',
        'list',
        'vms',
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    emulator = [vm for vm in unicode(output.rstrip(), "utf-8").split('\n') if 'AuroraOS' in vm]

    if not emulator:
        return ['', '']

    return (emulator[0]
            .replace('"', '')
            .replace('{', '')
            .replace('}', '')
            .split(' '))


# Startup vm virtualbox
def run_emulator_vm(key):
    subprocess.Popen([
        'VBoxManage',
        'startvm',
        key,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
