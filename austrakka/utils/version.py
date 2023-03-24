from functools import cmp_to_key
import requests
from semver import compare, VersionInfo
from loguru import logger

PYPI_PACKAGE_URI = 'https://pypi.org/pypi/austrakka/json'


def check_version(current):
    try:
        resp = requests.get(PYPI_PACKAGE_URI)
        releases = list(resp.json()['releases'].keys())
        latest = sorted(releases, key=cmp_to_key(compare))[-1]
        current_parsed = VersionInfo.parse(current)
        latest_parsed = VersionInfo.parse(latest)
        if latest_parsed.major > current_parsed.major:
            logger.critical(
                f"A new major version of 'austrakka' is available: "
                f"{latest} Please update immediately")
        elif latest_parsed.minor > current_parsed.minor:
            logger.error("A new minor version of 'austrakka' is available: "
                         f"{latest} Update to avoid any compatibility issues")
        elif latest_parsed.patch > current_parsed.patch:
            logger.warning("A new patch version of 'austrakka' is available: "
                           f"{latest}")
    except Exception as ex:
        logger.error(f"Error checking for new version : {ex}")
