from functools import cmp_to_key
import requests
from semver import compare, VersionInfo
from loguru import logger
from trakka import __prog_name__ as PROG_NAME

PYPI_PACKAGE_URI = f'https://pypi.org/pypi/{PROG_NAME}/json'


def check_version(current):
    try:
        resp = requests.get(PYPI_PACKAGE_URI, timeout=10)
        releases = list(resp.json()['releases'].keys())
        latest = sorted(releases, key=cmp_to_key(compare))[-1]
        current_parsed = VersionInfo.parse(current)
        latest_parsed = VersionInfo.parse(latest)
        if latest_parsed.major > current_parsed.major:
            logger.critical(
                f"A new major version of '{PROG_NAME}' is available: "
                f"{latest} Please update immediately")
        elif latest_parsed.minor > current_parsed.minor:
            logger.error(f"A new minor version of '{PROG_NAME}' is available: "
                         f"{latest} Update to avoid any compatibility issues")
        elif latest_parsed.patch > current_parsed.patch:
            logger.warning(f"A new patch version of '{PROG_NAME}' is available: "
                           f"{latest}")
    # pylint: disable=broad-exception-caught
    except Exception as ex:
        logger.warning(f"Error checking for new version : {ex}")
