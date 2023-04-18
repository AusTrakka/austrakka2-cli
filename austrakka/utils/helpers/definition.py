from austrakka.utils.paths import JOB_DEFINITION_PATH
from austrakka.utils.helpers import _get_by_identifier


def get_definition_by_name(name: str):
    return _get_by_identifier(JOB_DEFINITION_PATH, name)
