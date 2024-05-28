import os
from typing import List, Dict
import pandas as pd
from httpx import HTTPStatusError
from loguru import logger


from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_patch
from austrakka.utils.api import api_put
from austrakka.utils.exceptions import FailedResponseException, UnknownResponseException
from austrakka.utils.helpers.upload import upload_multipart
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe, log_response
from austrakka.utils.helpers.fields import get_system_field_names
from austrakka.utils.paths import PROFORMA_PATH
from austrakka.utils.retry import retry
from austrakka.utils.fs import FileHash, get_hash
from .proforma_generation_utils import generate_template
from ...utils.helpers.project import get_project_by_abbrev

ATTACH = 'Attach'


@logger_wraps()
def disable_proforma(abbrev: str):
    logger.info(f'Disabling pro forma: {abbrev}..')

    api_patch(
        path=f'{PROFORMA_PATH}/{abbrev}/disable',
    )

    logger.info('Done.')


@logger_wraps()
def enable_proforma(abbrev: str):
    logger.info(f'Enabling pro forma: {abbrev}..')

    api_patch(
        path=f'{PROFORMA_PATH}/{abbrev}/enable',
    )

    logger.info('Done.')


@logger_wraps()
def share_proforma(abbrev: str, group_names: List[str]):
    api_patch(
        path=f'{PROFORMA_PATH}/{abbrev}/share',
        data=group_names
    )

    logger.info('Done.')


@logger_wraps()
def unshare_proforma(abbrev: str, group_names: List[str]):
    api_patch(
        path=f'{PROFORMA_PATH}/{abbrev}/unshare',
        data=group_names
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

    pf_resp = api_get(
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

    api_put(
        path=f'{PROFORMA_PATH}/{pf_id}',
        data={
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

    return api_post(
        path=PROFORMA_PATH,
        data={
            "abbreviation": abbrev,
            "name": name,
            "description": description,
            "columnNames": column_names
        })


@logger_wraps()
def attach_proforma(abbrev: str,
                    filepath: str):
    """
    abbrev:
    file:
    """
    file_hash = get_hash(filepath)
    with open(filepath, 'rb') as file_content:
        files = [('files[]', (filepath, file_content))]

        custom_headers = {
            'proforma-abbrev': abbrev,
            'filename': os.path.basename(filepath),
        }
        try:
            retry(
                func=lambda f=files, fh=file_hash, ch=custom_headers: _post_proforma(f, fh, ch),
                retries=0,
                desc=f"{abbrev} at " + "/".join([PROFORMA_PATH, ATTACH]),
                delay=0.0
            )
        except FailedResponseException as ex:
            logger.error(f'Pro Forma {abbrev} failed upload')
            log_response(ex.parsed_resp)
        except (
                PermissionError, UnknownResponseException, HTTPStatusError
        ) as ex:
            logger.error(f'Pro Forma {abbrev} failed upload')
            logger.error(ex)


@logger_wraps()
def generate_proforma(
        abbrev: str, restrict: Dict[str, List[str]], nndss_column: bool, project_abbrev: str):
    "Generate an XLSX template for a pro forma"    
    # Get the pro forma spec
    response = api_get(
        path=f"{PROFORMA_PATH}/abbrev/{abbrev}"
    )
    field_df = _get_proforma_fields_df(response['data'])
    field_df.index = field_df['name']
    restricted_values = {
        field:sum([v.split(',') for v in valuestr.split(';')],[])
        for (field, valuestr) in restrict
    }
    project = None
    if project_abbrev:
        project = get_project_by_abbrev(project_abbrev)
    # Generate the spreadsheet
    filename = f"AusTrakka_metadata_submission_{abbrev}_DRAFT.xlsx"
    logger.info(f"Generating template draft {filename}")
    generate_template(filename, field_df, restricted_values, nndss_column, project)
    
   
def _get_proforma_fields_df(data):
    field_df = pd.DataFrame.from_dict(data['columnMappings'])[[
        'metaDataColumnName',
        'metaDataColumnDescription',
        'nndssFieldLabel',
        'metaDataColumnPrimitiveType',
        'metaDataColumnValidValues',
        'isRequired'
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

    field_df['type'].fillna('categorical', inplace=True)
    field_df['nndssFieldLabel'].fillna('', inplace=True)
    field_df['description'].fillna('', inplace=True)
    field_df['isRequired'] = field_df['isRequired'].apply(
        lambda x: True if x=='True' else (False if x=='False' else x)
    )
    field_df['allowedValues'] = field_df['allowedValues'].apply(
        lambda x: ';'.join(x) if x else None
    )

    return field_df

@logger_wraps()
def pull_proforma(abbrev: str, n_previous: int = None):
    n_prev = n_previous if n_previous is not None else 1
    api_patch(path=f'{PROFORMA_PATH}/PullPrevious/{abbrev}?nPrevious={n_prev}')
    logger.info('Done')


@logger_wraps()
def list_proformas(out_format: str):
    response = api_get(
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

    print_dataframe(
        result,
        out_format,
    )


@logger_wraps()
def show_proforma(abbrev: str, out_format: str):
    response = api_get(
        path=f"{PROFORMA_PATH}/abbrev/{abbrev}"
    )
    data = response['data'] if ('data' in response) else response

    for field in ['abbreviation', 'name', 'version', 'description']:
        logger.info(f'{field}: {data[field]}')

    logger.info('Pro forma fields:')

    field_df = _get_proforma_fields_df(data)
    
    print_dataframe(
        field_df,
        out_format,
    )


@logger_wraps()
def list_groups_proforma(abbrev: str, out_format: str):
    response = api_get(
        path=f"{PROFORMA_PATH}/{abbrev}/listgroups"
    )
    data = response['data'] if ('data' in response) else response

    if not data:
        logger.info("This pro forma is not shared with any groups.")
        return

    result = pd.DataFrame.from_dict(data)

    result.drop(['created',
                 'lastUpdated',
                 'lastUpdatedBy',
                 'createdBy',
                 'organisation',
                 'groupId'],
                axis='columns',
                inplace=True)

    print_dataframe(
        result,
        out_format,
    )


def _post_proforma(files, file_hash: FileHash, custom_headers: dict):
    upload_multipart(path="/".join([PROFORMA_PATH, ATTACH]),
                     files=files,
                     file_hash=file_hash,
                     custom_headers=custom_headers)
