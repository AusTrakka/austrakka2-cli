import requests
from semver import Version
from loguru import logger

PYPI_PACKAGE_URI = 'https://pypi.org/pypi/austrakka/json'


def check_version(current):
    try:
        resp = requests.get(PYPI_PACKAGE_URI, timeout=10)
        releases = list(resp.json()['releases'].keys())
        latest = sorted(releases)[-1]
        current_parsed = Version.parse(current)
        latest_parsed = Version.parse(latest)
        if latest_parsed.major > current_parsed.major:
            logger.warning(
                f"A new major version of 'austrakka' is available: "
                f"{latest} Please update immediately")
        elif latest_parsed.minor > current_parsed.minor:
            logger.warning("A new minor version of 'austrakka' is available: "
                         f"{latest} Update to avoid any compatibility issues")
        elif latest_parsed.patch > current_parsed.patch:
            logger.warning("A new patch version of 'austrakka' is available: "
                           f"{latest}")
    # pylint: disable=broad-exception-caught
    except Exception as ex:
        logger.warning(f"Error checking for new version : {ex}")
