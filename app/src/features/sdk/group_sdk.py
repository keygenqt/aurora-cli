import re
import click
import requests


@click.group(name='sdk')
def group_sdk():
    """Working with the Aurora SDKs."""
    pass


def _get_sdk_urls(url, is_url_path=True):
    response = requests.get(url)
    if response.status_code != 200:
        return []
    return list(reversed(
        [item for item in re.findall(r'href=[\'"]?([^\'" >]+)', response.text) if
         (not is_url_path or '-' not in item) and '..' not in item]))


def _get_versions(sdk_type):
    root = 'https://sdk-repo.omprussia.ru/sdk/installers/'
    sdk = ('PlatformSDK/', 'AppSDK/')[sdk_type == 'sdk']

    urls = _get_sdk_urls(root)
    versions = {}

    for url in urls:
        level2 = _get_sdk_urls(f"{root}{url}{sdk}")
        if level2:
            for item in level2:
                versions[item] = f"{root}{url}{sdk}"

    return versions


@group_sdk.command()
@click.option('--sdk-type', default='psdk', type=click.Choice(['sdk', 'psdk'], case_sensitive=False))
def available(sdk_type):
    """Get available version Aurora SDK or Platform SDK."""
    name = ('Platform SDK', 'Aurora SDK')[sdk_type == 'sdk']
    versions = _get_versions(sdk_type).keys()
    result = '\n'.join([str(item).replace('/', '') for item in versions])
    click.echo('Available {} versions:\n{}'.format(name, result))


@group_sdk.command()
@click.option('--sdk-type', default='psdk', type=click.Choice(['sdk', 'psdk'], case_sensitive=False))
def download(sdk_type):
    """Install Aurora SDK or Platform SDK."""
    name = ('Platform SDK', 'Aurora SDK')[sdk_type == 'sdk']
    versions = _get_versions(sdk_type)

    result = '\n'.join(
        ['{}: {}'.format(index + 1, str(item).replace('/', '')) for index, item in enumerate(versions.keys())])
    click.echo('Select index {} versions:\n{}'.format(name, result))

    index = -1
    while index < 0:
        index = click.prompt('Select version for download', type=int)
        if index > len(versions) or index <= 0:
            click.echo(f"Error: '{index}' is not a valid index.", err=True)
            index = -1

    key = list(versions.keys())[index - 1]
    url = '{}{}'.format(versions[key], key)
    urls = _get_sdk_urls(url, False)

    if sdk_type == 'sdk':
        files = [item for item in urls if 'run' in item and 'offline' in item]
    else:
        files = [item for item in urls if 'md5sum' not in item]

    files_url = ['{}{}'.format(url, item) for item in files]

    click.echo('\n'.join(files_url))

    # r = requests.get(url, stream=True)
    # path = '/some/path/for/file.txt'
    # with open(path, 'wb') as f:
    #     total_length = int(r.headers.get('content-length'))
    #     for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
    #         if chunk:
    #             f.write(chunk)
    #             f.flush()
