import requests
from bs4 import BeautifulSoup

from aurora_cli.src.support.helper import check_string_regex
from aurora_cli.src.support.output import echo_stdout
from aurora_cli.src.support.texts import AppTexts

# Url Aurora SDK
URL_AURORA_REPO = 'https://sdk-repo.omprussia.ru/sdk/installers/'

# Url Flutter SDK
URL_FLUTTER_SDK = 'https://gitlab.com/api/v4/projects/53055476/repository/tags?per_page=50'


# Get list versions Aurora SDK
def get_versions_sdk() -> []:
    versions = []
    echo_stdout(AppTexts.loading_server())
    response = requests.get(URL_AURORA_REPO)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for item in soup.findAll('a'):
            text = item.text.replace('/', '')
            if check_string_regex(text, [r'\d.\d.\d']):
                versions.append(text)
    versions.reverse()
    return versions[:3]


# Get list versions flutter
def get_versions_flutter() -> []:
    echo_stdout(AppTexts.loading_server())
    response = requests.get(URL_FLUTTER_SDK)
    return [obj['name'] for obj in response.json()]
