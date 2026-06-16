

from typing import List
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ORG_V2_PATH


@logger_wraps()
def list_metadata(identifier: str, out_format: str):
    call_get_and_print(
        f'{ORG_V2_PATH}/{identifier}/Metadata',
        out_format,
    )

@logger_wraps()
def list_metadata_by_field(identifier: str, field_names: List[str], out_format: str):
    call_get_and_print(
        f'{ORG_V2_PATH}/{identifier}/Metadata/Fields',
        out_format,
        params={
            'fields': field_names
        }
    )
