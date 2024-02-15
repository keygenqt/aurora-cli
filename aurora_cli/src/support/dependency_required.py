# Request sudo permissions
import subprocess

from aurora_cli.src.support.output import echo_stderr
from aurora_cli.src.support.texts import AppTexts


# Check dependency for init
def check_dependency_init():
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_git())
        exit(1)
    try:
        subprocess.run(['sudo', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_sudo())
        exit(1)


# Check dependency ffmpeg
def check_dependency_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_ffmpeg())
        exit(1)


# Check dependency vscode
def check_dependency_vscode():
    try:
        subprocess.run(['code', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_vscode())
        exit(1)


# Check dependency gdb-multiarch
def check_dependency_gdb_multiarch():
    try:
        subprocess.run(['gdb-multiarch', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (Exception,):
        echo_stderr(AppTexts.error_dependency_gdb_multiarch())
        exit(1)
