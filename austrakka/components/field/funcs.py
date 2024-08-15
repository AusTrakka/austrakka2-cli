import pandas as pd

from loguru import logger

from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name
from austrakka.utils.helpers.fields import get_field_by_name
from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_patch
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_dataframe
from austrakka.utils.paths import METADATACOLUMN_PATH


@logger_wraps()
def list_fields(out_format: str):
    """
    List all metadata fields (MetaDataColumns) within AusTrakka.
    """
    response = api_get(
        path=METADATACOLUMN_PATH,
    )

    data = response['data'] if ('data' in response) else response
    result = pd.DataFrame.from_dict(data)

    if 'primitiveType' in result:
        result['primitiveType'] = result['primitiveType'].fillna('category')
    if 'metaDataColumnValidValues' in result:
        result['metaDataColumnValidValues'] = result['metaDataColumnValidValues'].apply(
            lambda x: ';'.join(x) if x else ''
        )

    print_dataframe(
        result,
        out_format,
    )


@logger_wraps()
def add_field(
        name: str,
        description: str,
        nndss_label: str,
        typename: str,
        can_visualise: bool,
        column_order: int,
        private: bool,
):
    """
    Add a field (MetaDataColumn) to AusTrakka.
    """
    fieldtype = get_fieldtype_by_name(typename)

    if can_visualise and typename in ["date", "number", "string"]:
        logger.warning(
            f"Setting viz flag on field {name} of type {typename}. "
            f"This may work poorly as colour visualisations are configured for a small "
            f"discrete set of values.")
    else:
        # Set visualisation behaviour based on field type
        # Here booleans and categoricals give True
        if typename == "string":
            logger.warning(
                f"Setting default of --no-viz on field {name} due to type {typename}. "
                f"If this string field should be allowed to be used for colour visualisations, "
                f"set --viz.")
        can_visualise = (typename not in ["date", "number", "string"])

    api_post(
        path=METADATACOLUMN_PATH,
        data={
            "ColumnName": name,
            "CanVisualise": can_visualise,
            "ColumnOrder": column_order,
            "MetaDataColumnTypeId": fieldtype["metaDataColumnTypeId"],
            "IsActive": True,
            "IsPrivate": private,
            "Description": description,
            "NndssFieldLabel": nndss_label,
        }
    )


@logger_wraps()
def update_field(
        name: str,
        new_name: str,
        description: str,
        nndss_label: str,
        typename: str,
        can_visualise: bool,
        column_order: int,
        is_private: bool,
):
    """
    Update a field (MetaDataColumn) within AusTrakka.

    name specifies the name of the field to modify. All other parameters are optional, and their
    corresponding values will only be updated if they are specified.
    """
    field = get_field_by_name(name)

    patch_fields = {}

    if new_name is not None:
        logger.warning(f"Updating field name from {name} to {new_name}")
        patch_fields["columnName"] = new_name

    if typename is not None:
        fieldtype = get_fieldtype_by_name(typename)
        patch_fields["metaDataColumnTypeId"] = fieldtype["metaDataColumnTypeId"]

    if can_visualise is not None:
        if can_visualise:
            if typename in ["date", "number", "string"]:
                logger.warning(
                    f"Setting viz flag on field {name} of type {typename}. "
                    f"This may work poorly as colour visualisations are configured for a "
                    f"small discrete set of values.")
        patch_fields["canVisualise"] = can_visualise

    if column_order is not None:
        patch_fields["columnOrder"] = column_order

    if description is not None:
        patch_fields["description"] = description

    if nndss_label is not None:
        patch_fields["nndssFieldLabel"] = nndss_label

    if is_private is not None:
        patch_fields["isPrivate"] = is_private

    api_patch(
        path=f"{METADATACOLUMN_PATH}/{field['metaDataColumnId']}",
        data=patch_fields
    )


@logger_wraps()
def list_field_groups(name: str, out_format: str):
    """List groups that a metadata field belongs to"""
    result = api_get(
        path=f"{METADATACOLUMN_PATH}/{name}/groups"
    )
    if len(result['data']) == 0:
        logger.info("Field does not belong to any groups.")
        return
    print_dataframe(
        pd.DataFrame(result['data']),
        out_format,
    )


@logger_wraps()
def list_field_projects(name: str, out_format: str):
    """List projects that a metadata field belongs to"""
    result = api_get(
        path=f"{METADATACOLUMN_PATH}/{name}/projectFields"
    )
    if len(result['data']) == 0:
        logger.info("Field does not belong to any projects.")
        return
    display_columns = ['projectFieldId', 'projectAbbrev', 'fieldName', 'analysisLabels']
    print_dataframe(
        pd.DataFrame(result['data'])[display_columns],
        out_format,
    )


@logger_wraps()
def list_field_proformas(name: str, out_format: str):
    """List proformas that a metadata field belongs to"""
    result = api_get(
        path=f"{METADATACOLUMN_PATH}/{name}/proformas"
    )
    if len(result['data']) == 0:
        logger.info("Field does not belong to any active proformas.")
        return
    display_columns = ['proFormaId', 'proFormaVersionId', 'abbreviation', 'name', 'description',
                       'isActive', 'isCurrent']
    data = pd.DataFrame(result['data'])[display_columns]
    data['fieldIsRequired'] = [
        [mapping['isRequired'] for mapping in row['columnMappings']
         if mapping['metaDataColumnName'] == name][0]
        for row in result['data']
    ]

    print_dataframe(
        data,
        out_format,
    )


@logger_wraps()
def disable_field(name: str):
    """
    Disable a field (MetaDataColumn) within AusTrakka.
    """
    api_patch(
        path=f"{METADATACOLUMN_PATH}/{name}/disable"
    )


@logger_wraps()
def enable_field(name: str):
    """
    Enable a field (MetaDataColumn) within AusTrakka.
    """
    api_patch(
        path=f"{METADATACOLUMN_PATH}/{name}/enable"
    )
