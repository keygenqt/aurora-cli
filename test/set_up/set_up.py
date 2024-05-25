import subprocess


def emulator_off():
    names = [item.replace('"', '').split(' ')[0] for item in subprocess.run(
        'VBoxManage list runningvms',
        shell=True,
        text=True,
        capture_output=True
    ).stdout.split('\n') if item and 'AuroraOS']
    if names:
        subprocess.run(
            f'VBoxManage controlvm "{names[0]}" poweroff',
            shell=True,
            text=True,
            capture_output=True
        )
