import click

from app.src.features.sdk.impl.utils import get_string_from_list


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command()
@click.pass_context
def available(ctx):
    """Get available devices from configuration."""

    devices = ctx.obj.get_devices()
    click.echo('Available devices:\n{}'
               .format(get_string_from_list(devices.keys())))
