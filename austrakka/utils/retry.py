from loguru import logger


def retry(func, retries, desc):
    succeeded = False
    tried = 0
    while (tried <= retries) and not succeeded:
        try:
            func()
            succeeded = True
        # pylint: disable=broad-exception-caught
        except Exception as ex:
            logger.warning(f"Retry failed for '{desc}'")
            if tried >= retries:
                logger.warning(
                    f"Exhausted all retries for '{desc}'. Giving up.")
                raise ex
            tried = tried + 1
