import click
from .auth import auth

DEVELOPMENT_ENV = 'dev'


class HandleTopLevelParams(click.Group):
    # pylint: disable=super-with-arguments
    def parse_args(self, ctx, args):
        try:
            return super(HandleTopLevelParams, self).parse_args(ctx, args)
        except click.MissingParameter:
            # if getting help or trying to authorise, ignore top level params
            if '--help' not in args and args[0] != auth.name:
                raise
            # remove the required params so that help can display
            for param in self.params:
                param.required = False
            return super(HandleTopLevelParams, self).parse_args(ctx, args)


def is_dev_env(env: str):
    return env == DEVELOPMENT_ENV
