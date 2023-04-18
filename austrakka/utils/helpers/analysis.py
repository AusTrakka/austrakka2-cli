from austrakka.utils.paths import ANALYSIS_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_analysis_by_abbrev(abbrev: str):
    return _get_by_identifier(f'{ANALYSIS_PATH}/abbrev', abbrev)
