import os
import click
import requests


@click.group(name='flutter')
def group_flutter():
    """Working with the flutter."""
    pass


@group_flutter.command()
def available():
    """Get list available versions Flutter SDK."""

    response = requests.get('https://gitlab.com/api/v4/projects/53055476/repository/tags?per_page=50')
    tags = '\n'.join(obj['name'] for obj in response.json())
    click.echo('Available Flutter SDK versions:\n{}'.format(tags))
