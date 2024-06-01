from pathlib import Path


def get_version_sdk_from_file(file: Path) -> str | None:
    with open(file) as f:
        for line in f:
            if 'SDK_RELEASE=' in line:
                return line.split('=')[1].replace('-base', '').strip().strip('"')
    return None


def get_tool_sdk_from_file_with_version(file_version: Path) -> Path | None:
    tool_path = file_version.parent / 'SDKMaintenanceTool'
    if tool_path.is_file():
        return tool_path
    return None
