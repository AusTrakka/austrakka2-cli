from typing import List
from trakka.components.proforma.funcs import get_proforma_fields_df
from trakka.utils.api import api_get, api_patch
from trakka.utils.output import print_dataframe
from trakka.utils.paths import PROFORMA_PATH


def update_field(
        identifier: str, 
        field_identifier: str,
        metadata_class: str,
        clear_values: bool,
):
    api_patch(
        path=f'{PROFORMA_PATH}/{identifier}/Field',
        data={
            field_identifier: {
                "class": metadata_class,
                "clearValues": clear_values,
            }
        },
    )


def add_field_values(
        identifier: str, 
        field_identifier: str,
        values: List[str],
):
    api_patch(
        path=f'{PROFORMA_PATH}/{identifier}/Field/AddValues',
        data={
            field_identifier: {
                "values": values,
            }
        },
    )


def remove_field_values(
        identifier: str, 
        field_identifier: str,
        values: List[str],
):
    api_patch(
        path=f'{PROFORMA_PATH}/{identifier}/Field/RemoveValues',
        data={
            field_identifier: {
                "values": values,
            }
        },
    )


def list_fields(abbrev: str, out_format: str):
    response = api_get(
        path=f"{PROFORMA_PATH}/{abbrev}"
    )

    field_df = get_proforma_fields_df(response['data'])
    
    print_dataframe(
        field_df,
        out_format,
    )
