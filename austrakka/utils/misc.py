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
            if exc.param.name == CxtKey.CTX_TOKEN.value:
                click.echo(MISSING_TOKEN_HELP)
            elif exc.param.name == CxtKey.CTX_URI.value:
                click.echo(MISSING_URI_HELP)
            else:
                exc.ctx = None
                exc.show(file=sys.stdout)
            sys.exit(exc.exit_code)


def _get_custom_help_record(orig_help, multiple):
    if multiple:
        tmp_list = list(orig_help)
        split_str = tmp_list[len(tmp_list) - 1].rsplit("]", 1)
        if len(split_str) > 1:
            tmp_list[len(tmp_list) - 1] = split_str[0] + ";Accepts Multiple]"
        else:
            tmp_list[len(tmp_list) - 1] += " [Accepts Multiple]"
        orig_help = tuple(tmp_list)
    return orig_help


class AusTrakkaCliOption(click.Option):
    def get_help_record(self, ctx):
        orig_help = super().get_help_record(ctx)
        return _get_custom_help_record(orig_help, self.multiple)


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
