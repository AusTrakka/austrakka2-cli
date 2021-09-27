import os
import sys

import click
from loguru import logger

DEVELOPMENT_ENV = 'dev'


class CatchAllExceptions(click.Group):

    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except Exception as exc:
            if os.environ.get("AUSTRAKKA_ENV") == DEVELOPMENT_ENV:
                logger.exception(exc)
                logger.remove()
                logger.add(sys.stderr, level="DEBUG")
            else:
                logger.exception(exc)
                # Set default log level to INFO
                logger.remove()
                logger.add(sys.stderr, level="INFO")
            exit(1)
