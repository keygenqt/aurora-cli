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
from os.path import basename
from threading import Thread
from urllib.request import urlretrieve

from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import OutResult, OutResultInfo, OutResultError
from aurora_cli.src.base.utils.path import path_get_download_folder


def downloads(
        urls: [],
        listen_progress: Callable[[OutResult], None]
):
    out_exit = []
    out_percent_res = []
    out_percent_url = {}

    socket.setdefaulttimeout(10)

    def listen_out(url: str, percent: int):
        if percent < 0:
            if len(out_exit) == 1:
                if out_percent_url:
                    listen_progress(OutResultError(
                        message=TextError.download_error(),
                        value=url
                    ))
                else:
                    listen_progress(OutResultError(
                        message=TextError.start_download_error(),
                        value=url
                    ))
            return
        out_percent_url[url] = percent
        percent = int(sum(out_percent_url.values()) / len(urls))
        if percent in out_percent_res:
            return
        out_percent_res.append(percent)
        listen_progress(OutResultInfo(
            message=TextInfo.download_progress(),
            value=percent
        ))

    def worker(url_download: str, listen: Callable[[str, int], None]):
        percent_out = []
        path_download = path_get_download_folder() / basename(url_download)
        try:

            def reporthook(block_num, block_size, total_size):
                if True in out_exit:
                    path_download.unlink(missing_ok=True)
                    exit(1)
                percent = int(block_num * block_size * 100 / total_size)
                if percent in percent_out:
                    return
                percent_out.append(percent)
                listen(url_download, percent)

            urlretrieve(url_download, path_download, reporthook)
        except (Exception,):
            path_download.unlink(missing_ok=True)
            listen(url_download, -1)
            out_exit.append(True)

    for item in urls:
        thread = Thread(target=worker, args=[item, listen_out])
        thread.start()
