from pathlib import Path


def get_version_psdk_from_file(file: Path) -> str | None:
    with open(file) as f:
        for line in f:
            if 'PRETTY_NAME=' in line:
                return line.split('=')[1].strip().strip('"')
    return None


def get_tool_psdk_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent.parent / 'sdk-chroot'
    if tool_path.is_file():
        return tool_path
    return None
