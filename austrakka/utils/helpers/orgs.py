from austrakka.utils.paths import ORG_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_org_by_abbrev(abbrev: str):
    return _get_by_identifier(ORG_PATH, abbrev)
