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
from enum import Enum
from pathlib import Path
from threading import Thread
from time import sleep
from typing import Callable
from urllib.request import urlretrieve

from aurora_cli.src.base.constants.app import TIMEOUT
from aurora_cli.src.base.localization.localization import localization_abort
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.texts.success import TextSuccess
from aurora_cli.src.base.utils.alive_bar_percentage import AliveBarPercentage
from aurora_cli.src.base.utils.app import app_exit, app_abort_handler
from aurora_cli.src.base.utils.output import echo_stdout, OutResultError, OutResultInfo, OutResult
from aurora_cli.src.base.utils.path import path_get_download_path, path_convert_relative
from aurora_cli.src.base.utils.request import request_check_url_download
from aurora_cli.src.base.utils.verbose import verbose_add_map, verbose_command_start


def check_downloads(urls: []):
    files = []
    downloads_urls = []
    for url in urls:
        result = request_check_url_download(url)
        if result.is_error():
            echo_stdout(result)
            app_exit()
        files.append(path_get_download_path(result.value))
        echo_stdout(result)
        if result.is_success():
            downloads_urls.append(url)
    return downloads_urls, files


def check_with_download_files(
        files: [str],
        urls: [str],
        is_bar: bool = True
) -> [Path]:
    paths = []
    downloads_urls = []
    for i, file in enumerate(files):
        path = path_convert_relative(file)
        if not path.is_file() and len(urls) > i:
            downloads_urls.append(urls[i])

    if downloads_urls:
        echo_stdout(OutResultInfo(TextInfo.file_check_and_download()))
        downloads(downloads_urls, is_bar)

    for i, file in enumerate(files):
        path = path_convert_relative(file)
        if not path.is_file() and len(urls) > i:
            path_download = path_get_download_path(urls[i])
            path_download.replace(path)
        paths.append(path)

    return paths


def downloads(
        urls: [],
        is_bar: bool = True
):
    abort = []
    bar = AliveBarPercentage()

    def bar_update(result: int):
        if result == DownloadCode.start.value:
            bar.stop()
            echo_stdout(OutResultError(TextError.start_download_error()))
            exit(1)
        elif result == DownloadCode.download.value:
            bar.stop()
            echo_stdout(OutResultError(TextError.download_error()))
            exit(1)
        elif result == DownloadCode.interrupted.value:
            bar.stop()
            if not is_bar:
                echo_stdout(OutResultError(TextError.abort_download_error()))
            abort.append(True)
        elif result == DownloadCode.end.value:
            echo_stdout(OutResult(TextSuccess.download_success()))
        else:
            if is_bar:
                bar.update(result)
            else:
                echo_stdout(OutResultInfo(TextInfo.download_progress(), value=result))

    _downloads(urls, lambda result: bar_update(result))

    if True in abort:
        localization_abort()
        exit(1)


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

    app_abort_handler(lambda: out_abort.append(True))
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
            threads.clear()
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
            if block_size > total_size:
                sleep(1)
            if True in out_exit or True in out_abort:
                download_exit()
            percent = int(block_num * block_size * 100 / total_size)
            if percent > 100:
                percent = 100
            if percent in percent_out:
                return
            percent_out.append(percent)
            worker_listen(url_download, percent)
            if percent == 100:
                exit(0)

        command = verbose_command_start(f'urlretrieve: {url_download}')
        try:
            urlretrieve(url_download, path_download, reporthook)
            verbose_add_map(
                command=command,
                stdout=[],
                stderr=[],
            )
        except Exception as e:
            verbose_add_map(
                command=command,
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
