import click
import requests


@click.group(name='flutter')
def group_flutter():
    """Working with the Flutter SDK for Aurora OS."""
    pass


@group_flutter.command()
def available():
    """Get available versions flutter."""

    response = requests.get('https://gitlab.com/api/v4/projects/53055476/repository/tags?per_page=50')
    tags = '\n'.join(obj['name'] for obj in response.json())
    click.echo('Available Flutter SDK versions:\n{}'.format(tags))
