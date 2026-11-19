from typing import List, Dict
import pandas as pd
from loguru import logger

from trakka.utils.api import api_get
from trakka.utils.api import api_post
from trakka.utils.api import api_patch
from trakka.utils.api import api_put
from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.misc import logger_wraps
from trakka.utils.output import print_dataframe, get_viewtype_columns
from trakka.utils.paths import PROFORMA_PATH
from trakka.utils.privilege import ORG_RESOURCE, PROJECT_RESOURCE

UPDATE = 'update'
list_compact_fields = ['proFormaId', 'abbreviation', 'name', 'version', 'isActive']
list_more_fields = [
    'proFormaId',
    'abbreviation',
    'name',
    'description',
    'version',
    'hasAttached',
    'isActive']

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
def update_proforma(abbrev: str, name: str, description: str):
    # If both Name and Description are null or empty, it is an error
    if not name and not description:
        raise ValueError("Name and Description cannot both be empty")
    
    data = {}
    if name:
        data['name'] = name

    if description:
        data['description'] = description

    api_patch(
        path=f'{PROFORMA_PATH}/{abbrev}/{UPDATE}',
        data=data,
    )


@logger_wraps()
def add_version_proforma(
        abbrev: str,
        required_columns: List[str],
        optional_columns: List[str],
        remove_field: List[str],
        inherit: bool):

    _validate_add_version_args(inherit, required_columns, optional_columns, remove_field)

    data = api_get(path=f'{PROFORMA_PATH}/{abbrev}')['data']

    current_field_spec = {field['metaDataColumnName']: field['isRequired']
                          for field in data['columnMappings']}

    field_spec = _build_field_spec(
        current_field_spec,
        required_columns,
        optional_columns,
        remove_field,
        inherit
    )

    if field_spec == current_field_spec:
        logger.info("The specified pro forma fields are identical to the "
                    "current version. No update will be performed.")
        return

    column_names = [
        {"name": name, "isRequired": is_required}
        for name, is_required in field_spec.items()
    ]

    if not column_names:
        raise ValueError("A pro forma must contain at least one field")

    logger.info(f'Updating pro forma: {abbrev} with {len(column_names)} fields')

    api_put(
        path=f'{PROFORMA_PATH}/{abbrev}',
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
def list_proformas(view_type: str, out_format: str):
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

    # pylint: disable=duplicate-code
    columns = get_viewtype_columns(view_type, list_compact_fields, list_more_fields)
    print_dataframe(
        result,
        out_format,
        columns
    )


@logger_wraps()
def show_proforma(abbrev: str, out_format: str):
    call_get_and_print(f"{PROFORMA_PATH}/{abbrev}", out_format)


def _validate_add_version_args(
        inherit: bool,
        required_columns: List[str],
        optional_columns: List[str],
        remove_field: List[str]):
    conflicting_fields = set(required_columns) & set(optional_columns)
    if conflicting_fields:
        raise ValueError(
            "The following fields have been specified as both required and optional: "
            f"{', '.join(conflicting_fields)}"
        )
    conflicting_fields = (set(required_columns) | set(optional_columns)) & set(remove_field)
    if conflicting_fields:
        raise ValueError(
            "The following fields have been specified as both to be added/updated and removed: "
            f"{', '.join(conflicting_fields)}"
        )
    if not inherit and len(remove_field) > 0:
        raise ValueError(
            "The 'remove-field' option can only be used when 'inherit' is set."
        )

def _build_field_spec(
        current_field_spec: Dict[str, bool],
        required_columns: List[str],
        optional_columns: List[str],
        remove_field: List[str],
        inherit: bool) -> Dict[str, bool]:

    field_spec = {}
    if inherit:
        logger.info("Inheriting fields from previous version")
        field_spec = current_field_spec.copy()

    for field_name in required_columns:
        field_spec[field_name] = True

    for field_name in optional_columns:
        field_spec[field_name] = False

    for field_name in remove_field:
        if field_name in field_spec:
            del field_spec[field_name]
        else:
            logger.warning(
                f"Field '{field_name}' specified for removal was not found in the pro forma."
            )
    
    return field_spec


@logger_wraps()
def list_entities(identifier: str, entity_type: str, out_format: str):
    if entity_type not in [ORG_RESOURCE, PROJECT_RESOURCE]:
        raise ValueError(f"entity_type must be {ORG_RESOURCE} or {PROJECT_RESOURCE}")
    
    path = ""
    if entity_type == ORG_RESOURCE:
        path = f'{PROFORMA_PATH}/{identifier}/orgs'
    else:
        path = f'{PROFORMA_PATH}/{identifier}/projects'

    call_get_and_print(path, out_format)


@logger_wraps()
def share_entities(identifier: str, entity_type: str, entity_identifiers: List[str]):
    if entity_type not in [ORG_RESOURCE, PROJECT_RESOURCE]:
        raise ValueError(f"entity_type must be {ORG_RESOURCE} or {PROJECT_RESOURCE}")
    
    path = ""
    if entity_type == ORG_RESOURCE:
        path = f'{PROFORMA_PATH}/{identifier}/share/org'
    else:
        path = f'{PROFORMA_PATH}/{identifier}/share/project'

    api_patch(
        path=path,
        data=entity_identifiers,
    )


@logger_wraps()
def unshare_entities(identifier: str, entity_type: str, entity_identifiers: List[str]):
    if entity_type not in [ORG_RESOURCE, PROJECT_RESOURCE]:
        raise ValueError(f"entity_type must be {ORG_RESOURCE} or {PROJECT_RESOURCE}")
    
    path = ""
    if entity_type == ORG_RESOURCE:
        path = f'{PROFORMA_PATH}/{identifier}/unshare/org'
    else:
        path = f'{PROFORMA_PATH}/{identifier}/unshare/project'

    api_patch(
        path=path,
        data=entity_identifiers,
    )
