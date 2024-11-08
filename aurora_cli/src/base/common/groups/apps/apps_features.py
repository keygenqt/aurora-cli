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
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.app import app_exit
from aurora_cli.src.base.utils.argv import argv_is_api
from aurora_cli.src.base.utils.download import check_downloads, downloads
from aurora_cli.src.base.utils.output import echo_stdout, OutResultInfo


def apps_available_common():
    echo_stdout(TextInfo.available_versions_apps(request_versions_applications()))


def apps_download_common(app_id, arch):
    is_bar = not argv_is_api()
    apps = request_versions_applications()

    if app_id not in apps.keys():
        # @todo
        app_exit()

    app = apps[app_id]
    version = [version for version in app['versions'] if version['arch'] == arch]

    if not version:
        # @todo
        app_exit()

    url = version[0]['url']

    # check download urls
    urls, files = check_downloads([url], is_check_size=False)

    if not urls and not files:
        # @todo
        app_exit()

    if urls:
        echo_stdout(OutResultInfo(TextInfo.psdk_download_start()))
        downloads(urls, is_bar)
        sleep(1)

    for file in files:
        if not file.is_file():
            # @todo
            app_exit()

    return files[0]
