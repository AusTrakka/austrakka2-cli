import functools

import click
from loguru import logger

from ..components.auth import auth

DEVELOPMENT_ENV = 'dev'

HELP_OPTS = ['-h', '--help']


class HandleTopLevelParams(click.Group):
    # pylint: disable=super-with-arguments
    def parse_args(self, ctx, args):
        try:
            return super(HandleTopLevelParams, self).parse_args(ctx, args)
        except click.MissingParameter:
            # if getting help or trying to authorise, ignore top level params
            if not any(i in HELP_OPTS for i in args) and args[0] != auth.name:
                raise
            # remove the required params so that help can display
            for param in self.params:
                param.required = False
            return super(HandleTopLevelParams, self).parse_args(ctx, args)


def is_dev_env(env: str):
    return env == DEVELOPMENT_ENV


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
