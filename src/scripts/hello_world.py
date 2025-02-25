import click
from scripts.base import make_sync


@click.command(help="Hello World", name='hello-world')
@make_sync
async def hello_world():
    """Check the health of the bot."""
    click.echo("Hello World")