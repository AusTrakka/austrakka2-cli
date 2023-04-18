from austrakka.utils.paths import GROUP_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_group_by_name(abbrev: str):
    return _get_by_identifier(GROUP_PATH, abbrev)
