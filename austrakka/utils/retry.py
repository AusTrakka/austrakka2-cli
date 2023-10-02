
from time import sleep
from loguru import logger


def retry_on_5xx(func, retries, desc, delay=0):
    tried = 0
    while tried <= retries:
        resp = func()
        if resp.status_code < 500:
            return resp

        logger.warning(f"Retry failed for '{desc}'. HTTP Status Code: '{resp.status_code}'")
        if tried >= retries:
            logger.warning(
                f"Exhausted all retries for '{desc}'. Error: '{resp.status_code}'. "
                f"Giving up.")
            resp.raise_for_status()
        tried = tried + 1
        sleep(delay)

    # This path should not happen but will if retries is 0
    # raise an error.


def retry(func, retries, desc, delay=0):
    succeeded = False
    tried = 0
    while (tried <= retries) and not succeeded:
        try:
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
            sleep(delay)
