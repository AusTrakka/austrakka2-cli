import click

DEVELOPMENT_ENV = 'dev'


class IgnoreRequiredWithHelp(click.Group):
    # pylint: disable=super-with-arguments
    def parse_args(self, ctx, args):
        try:
            return super(IgnoreRequiredWithHelp, self).parse_args(ctx, args)
        except click.MissingParameter:
            if '--help' not in args:
                raise

            # remove the required params so that help can display
            for param in self.params:
                param.required = False
            return super(IgnoreRequiredWithHelp, self).parse_args(ctx, args)


class IgnoreTokenRequired(click.Group):
    pass
    # TOOD: this needs to ignore the existance of the AT_TOKEN env var
