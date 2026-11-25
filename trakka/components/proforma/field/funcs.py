from typing import List
import pandas as pd
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

    field_df = _get_proforma_fields_df(response['data'])
    
    print_dataframe(
        field_df,
        out_format,
    )


def _get_proforma_fields_df(data):
    field_df = pd.DataFrame.from_dict(data['columnMappings'])[[
        'metaDataColumnName',
        'metaDataColumnDescription',
        'nndssFieldLabel',
        'metaDataColumnPrimitiveType',
        'metaDataColumnValidValues',
        'isRequired',
        'class'
    ]]

    field_df.rename(
        columns={
            'metaDataColumnName': 'name',
            'metaDataColumnDescription': 'description',
            'metaDataColumnPrimitiveType': 'type',
            'metaDataColumnValidValues': 'allowedValues',
        },
        inplace=True
    )

    field_df['type'] = field_df['type'].fillna('categorical')
    field_df['nnssFieldLabel'] = field_df['nndssFieldLabel'].fillna('')
    field_df['description'] = field_df['description'].fillna('')
    field_df['isRequired'] = field_df['isRequired'].apply(
        lambda x: True if x=='True' else (False if x=='False' else x)
    )
    field_df['allowedValues'] = field_df['allowedValues'].apply(
        lambda x: ';'.join(x) if x else None
    )

    return field_df
