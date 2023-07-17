import sys
from tempfile import NamedTemporaryFile
from tempfile import gettempdir

from loguru import logger

FORMAT = "<m>{time:YYYY:MM:DD HH:mm:ss.SSS}</m> | <lvl>{level}</lvl> | <lvl>{" \
         "message}</lvl> "

LOG_LEVEL_TRACE = "TRACE"
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_SUCCESS = "SUCCESS"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_CRITICAL = "CRITICAL"

LOG_LEVELS = [
    LOG_LEVEL_TRACE,
    LOG_LEVEL_DEBUG,
    LOG_LEVEL_INFO,
    LOG_LEVEL_SUCCESS,
    LOG_LEVEL_WARNING,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_CRITICAL,
]


def setup_logger(log_level: str, log: str):
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
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


def is_debug(log_level: str):
    return log_level in [LOG_LEVEL_DEBUG, LOG_LEVEL_TRACE]
