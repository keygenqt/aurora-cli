import click

from app.src.features.emulator.impl.vbox import get_emulator_vm, run_emulator_vm


@click.group(name='emulator')
def group_emulator():
    """Working with the emulator virtualbox."""
    pass


@group_emulator.command()
def available():
    """Get available emulator."""

    emulator_name, emulator_key = get_emulator_vm()

    if emulator_name:
        emulator = emulator_name.replace('-base', '').split('-')
        click.echo('Emulator virtualbox Aurora OS: {}'.format(emulator[1]))
    else:
        click.echo('Emulator virtualbox not found.')


@group_emulator.command()
def run():
    """Run emulator."""

    emulator_name, emulator_key = get_emulator_vm()

    if emulator_name:
        run_emulator_vm(emulator_key)
    else:
        click.echo('Emulator virtualbox not found.')
