import os
import sys

import click
from loguru import logger

DEVELOPMENT_ENV = 'dev'


class IgnoreRequiredWithHelp(click.Group):
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
