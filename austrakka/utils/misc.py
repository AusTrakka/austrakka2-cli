import functools
import sys

import click
from loguru import logger

from austrakka.components.auth import auth
from austrakka.utils.context import CxtKey


HELP_OPTS = ['-h', '--help']

MISSING_TOKEN_HELP = '''Error: Environment variable AT_TOKEN is not set.

This value can be obtained by running the following command:
austrakka auth user'''
MISSING_URI_HELP = '''Error: Environment variable AT_URI is not set.

Please contact an AusTrakka admin if you do not have this value.'''


class AusTrakkaCliTopLevel(click.Group):
    # pylint: disable=super-with-arguments
    def parse_args(self, ctx, args):
        try:
            return super(AusTrakkaCliTopLevel, self).parse_args(ctx, args)
        except click.MissingParameter:
            # if getting help or trying to authorise, ignore top level params
            if not any(i in HELP_OPTS for i in args) and args[0] != auth.name:
                raise
            # remove the required params so that help can display
            for param in self.params:
                param.required = False
            return super(AusTrakkaCliTopLevel, self).parse_args(ctx, args)

    # pylint: disable=inconsistent-return-statements
    def __call__(self, *args, **kwargs):
        try:
            return super(AusTrakkaCliTopLevel, self).__call__(
                *args, standalone_mode=False, **kwargs)
        except click.MissingParameter as exc:
            # If there is a missing top level parameter (eg. URI or TOKEN)
            # provide extended error message
            if exc.param.name == CxtKey.TOKEN.value:
                click.echo(MISSING_TOKEN_HELP)
            elif exc.param.name == CxtKey.URI.value:
                click.echo(MISSING_URI_HELP)
            else:
                exc.ctx = None
                exc.show(file=sys.stdout)
            sys.exit(exc.exit_code)


def logger_wraps(*, entry=True, exit_func=True):

    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if entry:
                logger.debug(
                    f"Entering '{name}' (args={args}, kwargs={kwargs})"
                )
            result = func(*args, **kwargs)
            if exit_func:
                logger.debug(f"Exiting '{name}' (result={result})")
            return result

        return wrapped

    return wrapper
