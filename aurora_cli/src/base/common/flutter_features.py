from pathlib import Path


def get_version_flutter_from_file(file: Path) -> str | None:
    with open(file) as f:
        for line in f:
            if '- Last tag:' in line:
                return line.split(':')[1].strip()
    return None


def get_tool_flutter_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent / 'bin' / 'flutter'
    if tool_path.is_file():
        return tool_path
    return None


def get_tool_dart_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent / 'bin' / 'dart'
    if tool_path.is_file():
        return tool_path
    return None
