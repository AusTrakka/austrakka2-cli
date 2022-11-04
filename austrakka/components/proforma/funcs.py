from typing import List

import pandas as pd
from loguru import logger

from austrakka.utils.api import call_api
from austrakka.utils.api import get, post, patch, put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_table
from austrakka.utils.helpers.fields import get_system_field_names
from austrakka.utils.paths import PROFORMA_PATH


@logger_wraps()
def disable_proforma(abbrev: str):
    logger.info(f'Disabling pro forma: {abbrev}..')

    call_api(
        method=patch,
        path=f'{PROFORMA_PATH}/{abbrev}/disable',
    )

    logger.info('Done.')


@logger_wraps()
def enable_proforma(abbrev: str):
    logger.info(f'Enabling pro forma: {abbrev}..')

    call_api(
        method=patch,
        path=f'{PROFORMA_PATH}/{abbrev}/enable',
    )

    logger.info('Done.')


@logger_wraps()
def share_proforma(abbrev: str, group_names: List[str]):
    call_api(
        method=patch,
        path=f'{PROFORMA_PATH}/{abbrev}/share',
        body=group_names
    )

    logger.info('Done.')


@logger_wraps()
def unshare_proforma(abbrev: str, group_names: List[str]):
    call_api(
        method=patch,
        path=f'{PROFORMA_PATH}/{abbrev}/unshare',
        body=group_names
    )

    logger.info('Done.')


@logger_wraps()
def update_proforma(
        abbrev: str,
        required_columns: List[str],
        optional_columns: List[str]):

    # Include system fields (avoid an error from the endpoint; don't force CLI user to type them in)
    # Note that we are not forcing system fields the user DOES include
    # to set IsRequired
    system_fields = get_system_field_names()
    missing_system_fields = [
        fieldname for fieldname in system_fields if fieldname not in required_columns +
        optional_columns]

    pf_resp = call_api(
        method=get,
        path=f'{PROFORMA_PATH}/abbrev/{abbrev}',
    )

    data = pf_resp['data'] if ('data' in pf_resp) else pf_resp
    pf_id = data['proFormaId']

    required_columns = list(required_columns)
    for field in missing_system_fields:
        logger.warning(
            f"System field {field} must be included: adding to pro forma")
        required_columns.append(field)

    column_names = (
        [{"name": col, "isRequired": True} for col in required_columns]
        + [{"name": col, "isRequired": False} for col in optional_columns])

    total_columns = len(column_names)

    if total_columns == 0:
        raise ValueError("A pro forma must contain at least one field")

    logger.info(f'Updating pro forma: {abbrev} with {total_columns} fields')

    call_api(
        method=put,
        path=f'{PROFORMA_PATH}/{pf_id}',
        body={
            "abbreviation": abbrev,
            "columnNames": column_names
        })

    logger.info('Done.')


@logger_wraps()
def add_proforma(
        abbrev: str,
        name: str,
        description: str,
        required_columns: List[str],
        optional_columns: List[str]):

    # Include system fields (avoid an error from the endpoint; don't force CLI user to type them in)
    # Note that we are not forcing system fields the user DOES include
    # to set IsRequired
    system_fields = get_system_field_names()
    missing_system_fields = [
        fieldname for fieldname in system_fields if fieldname not in required_columns +
        optional_columns]
    required_columns = list(required_columns)
    for field in missing_system_fields:
        logger.warning(
            f"System field {field} must be included: adding to pro forma")
        required_columns.append(field)

    column_names = (
        [{"name": col, "isRequired": True} for col in required_columns]
        + [{"name": col, "isRequired": False} for col in optional_columns])
    if len(column_names) == 0:
        raise ValueError("A pro forma must contain at least one field")

    return call_api(
        method=post,
        path=PROFORMA_PATH,
        body={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "columnNames": column_names
        })


@logger_wraps()
def list_proformas(out_format: str):
    response = call_api(
        method=get,
        path=PROFORMA_PATH,
        params={
            'includeall': False
        }
    )

    data = response['data'] if ('data' in response) else response

    if not data:
        logger.info("No pro formas available.")
        return

    result = pd.DataFrame.from_dict(data)

    result.drop(['columnMappings',
                 'proFormaVersionId',
                 'lastUpdatedBy',
                 'lastUpdated'],
                axis='columns',
                inplace=True)

    print_table(
        result,
        out_format,
    )


@logger_wraps()
def show_proformas(abbrev: str, out_format: str):
    response = call_api(
        method=get,
        path=f"{PROFORMA_PATH}/abbrev/{abbrev}"
    )
    data = response['data'] if ('data' in response) else response

    for field in ['abbreviation', 'name', 'version', 'description']:
        logger.info(f'{field}: {data[field]}')

    logger.info('Pro forma fields:')

    # Should add isActive check, but probably in endpoint
    field_df = pd.DataFrame.from_dict(data['columnMappings'])[
        ['metaDataColumnName', 'metaDataColumnPrimitiveType', 'isRequired']]

    field_df.rename(
        columns={'metaDataColumnPrimitiveType': 'type'},
        inplace=True
    )

    field_df['type'].fillna('categorical', inplace=True)
    print_table(
        field_df,
        out_format,
    )
