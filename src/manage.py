import click

from scripts import commands


@click.group()
def cli():
    """The root of commands."""
    pass


for command in commands:
    cli.add_command(command)


if __name__ == "__main__":
    cli()