import re

from bs4 import BeautifulSoup

from aurora_cli.src.base.constants.url import URL_AURORA_REPO_VERSIONS, URL_FLUTTER_SDK_VERSIONS, \
    URL_FLUTTER_PLUGINS_VERSIONS
from aurora_cli.src.base.texts.error import TextError
from aurora_cli.src.base.texts.info import TextInfo
from aurora_cli.src.base.utils.output import OutResult, OutResultError
from aurora_cli.src.base.utils.request import get_request


def _get_versions_from_repo(url: str) -> []:
    versions = []
    response = get_request(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if re.search(r'\d.\d.\d', text):
                versions.append(text)
    versions.reverse()
    return versions


def get_versions_sdk() -> OutResult:
    try:
        versions = _get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_sdk(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_versions_psdk() -> OutResult:
    try:
        versions = _get_versions_from_repo(URL_AURORA_REPO_VERSIONS)
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_psdk(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_versions_flutter() -> OutResult:
    try:
        response = get_request(URL_FLUTTER_SDK_VERSIONS)
        versions = [obj['name'] for obj in response.json()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())


def get_flutter_plugins() -> OutResult:
    try:
        response = get_request(URL_FLUTTER_PLUGINS_VERSIONS)
        versions = [obj['name'] for obj in response.json()]
        if not versions:
            return OutResultError(TextError.request_empty_error())
        return OutResult(TextInfo.available_versions_flutter(versions))
    except (Exception,):
        return OutResultError(TextError.request_error())
