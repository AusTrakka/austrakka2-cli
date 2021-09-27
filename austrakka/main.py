import click

from . import __version__ as VERSION
from .utils import CatchAllExceptions

from austrakka.auth import auth
from austrakka.user import user


@click.group(cls=CatchAllExceptions)
@click.option("--api-key", envvar='AUSTRAKKA_API_KEY', show_default=True, required=True)
@click.option("--uri", envvar='AUSTRAKKA_URI', required=True)
@click.option("--token", envvar='AUSTRAKKA_TOKEN', required=True)
@click.version_option(message="%(prog)s v%(version)s", version=VERSION)
@click.help_option("-h", "--help")
@click.pass_context
def cli(ctx, api_key, uri, token):
    """
    A cli for interfacing with AusTrakka from the command line.
    """
    ctx.creds = {'api_key': api_key, 'uri': uri, 'token': token}


cli.add_command(auth)
cli.add_command(user)

if __name__ == "__main__":
    cli()
