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
import socket
from collections.abc import Callable
from enum import Enum
from threading import Thread
from urllib.request import urlretrieve

import click

from aurora_cli.src.base.constants.app import TIMEOUT
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.abort import abort_catch
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, OutResult
from aurora_cli.src.base.utils.path import path_get_download_path
from aurora_cli.src.base.utils.request import request_check_url_download
from aurora_cli.src.base.utils.verbose import verbose_add_map


def check_downloads(urls: []):
    files = []
    downloads_url = []
    for url in urls:
        result = request_check_url_download(url)
        # Exit with has error with url
        if result.is_error():
            echo_stdout(request_check_url_download(url))
            exit(1)
        # Info - if file exist and ok
        if result.is_info():
            files.append(result.value)
            echo_stdout(request_check_url_download(url))
            continue
        # Ready for download
        files.append(result.value)
        downloads_url.append(url)
    return downloads_url, files


def downloads(
        urls: [],
        verbose: bool,
        is_bar: bool = True
):
    abort = []
    bar = AliveBarPercentage()

    def bar_update(result: int):
        match result:
            case DownloadCode.start.value:
                bar.stop()
                echo_stdout(OutResultError(TextError.start_download_error()), verbose)
            case DownloadCode.download.value:
                bar.stop()
                echo_stdout(OutResultError(TextError.download_error()), verbose)
            case DownloadCode.interrupted.value:
                bar.stop()
                if not is_bar:
                    echo_stdout(OutResultError(TextError.abort_download_error()), verbose)
                abort.append(True)
            case DownloadCode.end.value:
                echo_stdout(OutResult(TextSuccess.download_success()), verbose)
            case _:
                if is_bar:
                    bar.update(result)
                else:
                    echo_stdout(OutResultInfo(TextInfo.download_progress(), value=result), verbose)

    _downloads(urls, lambda result: bar_update(result))

    if True in abort:
        raise click.exceptions.Abort


class DownloadCode(Enum):
    start = -1
    download = -2
    interrupted = -3
    end = -4


def _downloads(
        urls: [],
        listen: Callable[[int], None]
):
    threads = []
    out_abort = []
    out_exit = []
    out_percent_res = []
    out_percent_url = {}

    abort_catch(lambda: out_abort.append(True))
    socket.setdefaulttimeout(TIMEOUT)

    def listen_out(url: str, percent: int):
        if percent < 0:
            if len(out_exit) == len(urls):
                if True in out_abort:
                    # Out abort
                    listen(DownloadCode.interrupted.value)
                else:
                    if out_percent_url:
                        # Out if error download
                        listen(DownloadCode.download.value)
                    else:
                        # Out if start error
                        listen(DownloadCode.start.value)
            return

        out_percent_url[url] = percent
        percent = int(sum(out_percent_url.values()) / len(urls))
        if percent in out_percent_res:
            return
        out_percent_res.append(percent)
        # Out ok - percent
        if percent == 100:
            listen(percent)
            listen(DownloadCode.end.value)
        else:
            listen(percent)

    def worker(url_download: str, worker_listen: Callable[[str, int], None]):
        percent_out = []
        path_download = path_get_download_path(url_download)

        def download_exit():
            out_exit.append(True)
            worker_listen(url_download, -1)
            path_download.unlink(missing_ok=True)
            exit(1)

        def reporthook(block_num, block_size, total_size):
            if True in out_exit or True in out_abort:
                download_exit()
            percent = int(block_num * block_size * 100 / total_size)
            if percent in percent_out:
                return
            percent_out.append(percent)
            worker_listen(url_download, percent)

        try:
            verbose_add_map(
                command=f'Download: {url_download}',
                stdout=[],
                stderr=[],
            )
            urlretrieve(url_download, path_download, reporthook)
        except Exception as e:
            verbose_add_map(
                command=f'Download: {url_download}',
                stdout=[],
                stderr=[str(e)],
            )
            download_exit()

    for item in urls:
        thread = Thread(target=worker, args=[item, listen_out], daemon=True)
        threads.append(thread)
        thread.start()
    for thr in threads:
        thr.join()
