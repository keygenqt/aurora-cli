import click

from app.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html
from app.src.features.sdk.impl.utils import get_string_from_list, get_string_from_list_numbered, prompt_index


@click.group(name='sdk')
def group_sdk():
    """Working with the Aurora SDK."""
    pass


@group_sdk.command()
def available():
    """Get available version Aurora SDK."""

    versions = get_map_versions(TypeSDK.SDK)

    click.echo('Available Aurora SDK versions:\n{}'
               .format(get_string_from_list(versions.keys())))


@group_sdk.command()
@click.option('-t', '--install-type', default='offline', type=click.Choice(['offline', 'online'], case_sensitive=False))
def download(install_type):
    """Download and run install Aurora SDK."""

    versions = get_map_versions(TypeSDK.SDK)

    click.echo('Select index Aurora SDK versions:\n{}\n'
               .format(get_string_from_list_numbered(versions.keys())))

    index = prompt_index(versions.keys())
    key = list(versions.keys())[index - 1]
    url = '{}{}'.format(versions[key], key)

    links = get_urls_on_html(url)
    files = [item for item in links if 'run' in item and install_type in item]
    files_url = ['{}{}'.format(url, item) for item in files]

    click.echo('\nDownload Aurora SDK links:\n{}'
               .format(get_string_from_list(files_url)))
