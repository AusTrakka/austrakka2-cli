from austrakka.utils.paths import METADATACOLUMNTYPE_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_fieldtype_by_name(name: str):
    return _get_by_identifier(f'{METADATACOLUMNTYPE_PATH}/name', name)
