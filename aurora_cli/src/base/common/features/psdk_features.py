"""
Copyright 2024 Vitaliy Zarubin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from pathlib import Path
from typing import Callable, Any

from aurora_cli.src.base.common.features.search_files import search_aurora_project_builds_rpm
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.percent_cli import percent_point, percent_start, percent_end
from aurora_cli.src.base.utils.shell import shell_exec_command, shell_check_error_out


def psdk_project_build(
        target: str,
        tool: str,
        clean: bool,
        debug: bool,
        path: Path,
        progress: Callable[[int], None]
) -> OutResult:
    percents = []
    percent_start(percents, progress)
    points = [
        'Mounting system directories',
        'Last login',
        'Resolving package dependencies',
        'Executing(%build)',
        'rpmlint session starts',
    ]

    def get_arch() -> Any:
        if 'aarch64' in target:
            return 'aarch64'
        if 'x86_64' in target:
            return 'x86_64'
        if 'armv7hl' in target:
            return 'armv7hl'
        return None

    arg = [
        tool,
        'mb2',
        '--no-fix-version',
        '--target',
        target,
        f'build',
    ]

    if debug:
        arg.append('-d')

    if clean:
        arg.append('--clean')

    if not debug:
        arg.append('--nodebuginfo')

    stdout, _ = shell_exec_command(
        arg,
        cwd=path,
        listen=lambda out: percent_point(out, points, percents, progress),
        disable_sigint=False
    )

    percent_end(percents, progress)

    result = shell_check_error_out(stdout, None, ['crash'])
    if result.is_error():
        return result

    arch = get_arch()
    if not arch:
        return OutResultError(TextError.arch_not_found())

    builds_paths = [str(path) for path in search_aurora_project_builds_rpm(path / 'RPMS', arch)]

    if not debug:
        builds_paths = [path for path in builds_paths if 'debuginfo' not in path and 'debugsource' not in path]

    return OutResult(TextSuccess.flutter_build_success(builds_paths), value=builds_paths)
