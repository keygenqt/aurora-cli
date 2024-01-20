import os
import click


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command()
@click.option('--index', default=None, type=click.INT, help='Select index')
@click.pass_context
def basename(ctx, index):
    """Show basename path."""
    click.echo(index)
    click.echo(os.path.basename(ctx.obj.path))

