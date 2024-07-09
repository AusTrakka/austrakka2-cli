
from time import sleep
from loguru import logger
from austrakka.utils.exceptions import FailedResponseException
from austrakka.utils.exceptions import UnknownResponseException

def retry(func, retries, desc, delay=0):
    succeeded = False
    tried = 0
    while (tried <= retries) and not succeeded:
        try:
            sleep(delay)
            func()
            succeeded = True
        # pylint: disable=broad-exception-caught
        except (UnknownResponseException,FailedResponseException) as ex:
            logger.warning(f"Retry failed for '{desc}'. Error: '{ex}'")
            # 404 not found, 409 conflict
            if hasattr(ex, 'status_code') and ex.status_code in [404, 409]:
                raise ex
            if tried >= retries:
                logger.warning(
                    f"Exhausted all retries for '{desc}'. Error: '{ex}'. "
                    f"Giving up.")
                raise ex
            tried = tried + 1
