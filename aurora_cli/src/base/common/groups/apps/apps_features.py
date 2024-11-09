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
from time import sleep

from aurora_cli.src.base.common.features.request_version import request_versions_applications
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.download import check_downloads, downloads
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo, OutResultError


def apps_available_common():
    echo_stdout(TextInfo.available_versions_apps(request_versions_applications()))


def apps_download_common(app_id, arch):
    is_bar = not argv_is_api()
    apps = request_versions_applications()

    if app_id not in apps.keys():
        echo_stdout(OutResultError(TextError.error_application_id(app_id)))
        app_exit()

    app = apps[app_id]
    build = [build for build in app['versions'] if build['arch'] == arch]

    if not build:
        echo_stdout(OutResultError(TextError.error_application_arch(arch)))
        app_exit()

    url = build[0]['url']
    urls, files = check_downloads([url], is_check_size=False)

    if not urls and not files:
        echo_stdout(OutResultError(TextError.get_install_info_error()))
        app_exit()

    if urls:
        echo_stdout(OutResultInfo(TextInfo.application_download_start()))
        downloads(urls, is_bar)
        sleep(1)

    for file in files:
        if not file.is_file():
            echo_stdout(OutResultError(TextError.get_install_info_error()))
            app_exit()

    return files[0]
