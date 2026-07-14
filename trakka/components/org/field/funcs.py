from typing import List

from trakka.utils.api import api_patch
from trakka.utils.misc import logger_wraps
from trakka.utils.output import get_viewtype_columns
from trakka.utils.paths import ORG_V2_PATH
from trakka.utils.helpers.output import call_get_and_print


@logger_wraps()
def add_field(identifier: str, field_names: List[str]):
    return api_patch(
        path=f'{ORG_V2_PATH}/{identifier}/Fields/Add',
        data={
            "fields": field_names
        }
    )


@logger_wraps()
def remove_field(identifier: str, field_names: List[str]):
    return api_patch(
        path=f'{ORG_V2_PATH}/{identifier}/Fields/Remove',
        data={
            "fields": field_names
        }
    )


@logger_wraps()
def list_field(identifier: str, out_format: str, view_type: str):
    compact_fields = [
        "columnName",
        "metaDataColumnTypeName",
        "description",
        "primitiveType",
        "isActive",
    ]
    columns = get_viewtype_columns(view_type, compact_fields, [])
    call_get_and_print(
        f'{ORG_V2_PATH}/{identifier}/Fields',
        out_format,
        restricted_cols=columns,
    )
