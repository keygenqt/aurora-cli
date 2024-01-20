import click

from app.src.features.sdk.impl.urls import get_map_versions, TypeSDK, get_urls_on_html
from app.src.features.sdk.impl.utils import get_string_from_list, get_string_from_list_numbered, prompt_index


@click.group(name='psdk')
def group_psdk():
    """Working with the Aurora Platform SDK."""
    pass


@group_psdk.command()
def available():
    """Get available version Aurora Platform SDK."""

    versions = get_map_versions(TypeSDK.PSDK)

    click.echo('Available Aurora Platform SDK versions:\n{}'
               .format(get_string_from_list(versions.keys())))


@group_psdk.command()
def download():
    """Download and run install Aurora Platform SDK."""

    versions = get_map_versions(TypeSDK.PSDK)

    click.echo('Select index Aurora Platform SDK versions:\n{}\n'
               .format(get_string_from_list_numbered(versions.keys())))

    index = prompt_index(versions.keys())
    key = list(versions.keys())[index - 1]
    url = '{}{}'.format(versions[key], key)

    links = get_urls_on_html(url)
    files = [item for item in links if 'md5sum' not in item]
    files_url = ['{}{}'.format(url, item) for item in files]

    click.echo('\nDownload Aurora Platform SDK links:\n{}'
               .format(get_string_from_list(files_url)))
