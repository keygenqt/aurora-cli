# Request sudo permissions
import subprocess


# Check dependency vscode plugin
def check_dependency_vscode_plugin(name: str) -> bool:
    output = subprocess.check_output(['code', '--list-extensions']).decode('utf-8')
    if name in output:
        return True
    return False


# Check dependency apt
def check_dependency_apt() -> bool:
    try:
        subprocess.run(['apt', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (Exception,):
        return False
