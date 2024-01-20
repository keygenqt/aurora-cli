import os
import click


@click.group(name='embedder')
def group_embedder():
    """Working with the embedder."""
    pass


@group_embedder.command()
@click.pass_context
def basename(ctx):
    """Show basename path."""
    click.echo(os.path.basename(ctx.obj.path))
