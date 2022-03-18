import sys
from tempfile import NamedTemporaryFile
from tempfile import gettempdir

from loguru import logger

from austrakka.utils.misc import is_dev_env

FORMAT = "<m>{time:YYYY:MM:DD HH:mm:ss.SSS}</m> | <lvl>{level}</lvl> | <lvl>{" \
         "message}</lvl> "


def setup_logger(env: str, log: str):
    logger.remove()
    logger.add(
        sys.stderr,
        level='DEBUG' if is_dev_env(env) else 'INFO',
        format=FORMAT
    )

    if log == 'file':
        logger.debug(f'Creating temp file in {gettempdir()}')
        # pylint: disable=consider-using-with
        log_file = NamedTemporaryFile(
            mode='w',
            prefix='austrakka-cli-output-',
            suffix='.log',
            delete=False
        )
        logger.info(f'Redirecting log output to {log_file.name}')
        logger.remove()
        logger.add(log_file.name)
