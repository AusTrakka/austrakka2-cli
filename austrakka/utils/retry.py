
from time import sleep
from loguru import logger


def retry(func, retries, desc, delay=0):
    succeeded = False
    tried = 0
    while (tried <= retries) and not succeeded:
        try:
            sleep(delay)
            func()
            succeeded = True
        # pylint: disable=broad-exception-caught
        except Exception as ex:
            logger.warning(f"Retry failed for '{desc}'. Error: '{ex}'")
            if tried >= retries:
                logger.warning(
                    f"Exhausted all retries for '{desc}'. Error: '{ex}'. "
                    f"Giving up.")
                raise ex
            tried = tried + 1
