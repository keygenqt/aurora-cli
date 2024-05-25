from pathlib import Path

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.dependency import check_dependency, DependencyApps
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.shell import shell_exec_command


@check_dependency(DependencyApps.ffmpeg)
def convert_video(v_path: Path, s_path: Path) -> OutResult:
    def check_is_error(outs: []) -> bool:
        for out in outs:
            if 'Unknown-sized element at' in out:
                return True
        return False

    stdout, stderr = shell_exec_command([
        'ffmpeg',
        '-i',
        str(v_path),
        '-c:v',
        'libx264',
        '-preset',
        'slow',
        '-crf',
        '22',
        '-c:a',
        'copy',
        '-b:a',
        '128k',
        str(s_path),
    ])
    if stderr or check_is_error(stdout):
        return OutResultError(TextError.emulator_recording_video_convert_error())
    return OutResult(
        message=TextSuccess.emulator_recording_video_convert(str(s_path)),
        value=str(s_path)
    )
