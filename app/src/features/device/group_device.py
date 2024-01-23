import click

from app.src.base.utils import get_string_from_list, get_string_from_list_numbered, prompt_index
from app.src.features.device.impl.ssh import get_ssh_clients


@click.group(name='device')
def group_device():
    """Working with the device."""
    pass


@group_device.command()
@click.pass_context
def available(ctx):
    """Get available devices from configuration."""

    devices = ctx.obj.get_devices()

    # Get connections
    clients = get_ssh_clients(devices)

    # Output
    if clients:
        click.echo('Available devices:\n{}'
                   .format(get_string_from_list(clients.keys())))
    else:
        click.echo('No active devices found.')


@group_device.command()
@click.pass_context
@click.option('-e', '--exec_command', type=click.STRING, required=True)
def command(ctx, exec_command):
    """Execute the command on the device."""

    devices = ctx.obj.get_devices()

    # Get connections
    clients = get_ssh_clients(devices)

    if not clients:
        click.echo(click.style('No active devices found', fg='red'))
        exit(1)

    if len(clients.keys()) != 1:
        click.echo('Found active devices:\n{}'
                   .format(get_string_from_list_numbered(clients.keys())))

    # Query index
    index = prompt_index(clients.keys())
    key = list(clients.keys())[index - 1]

    # Run command
    _, ssh_stdout, ssh_stderr = clients[key].exec_command(exec_command)

    # Output success
    title = True
    for line in iter(ssh_stdout.readline, ""):
        if title:
            click.echo('{} "{}" {}'.format(click.style('Command', fg='green'),
                                           exec_command,
                                           click.style('completed successfully:', fg='green')))
            title = False
        click.echo(line.strip())

    # Output errros
    for line in iter(ssh_stderr.readline, ""):
        if title:
            click.echo('{} "{}" {}'.format(click.style('Command', fg='red'),
                                           exec_command,
                                           click.style('was executed with an error:', fg='red')))
            title = False
        click.echo(line.strip())
