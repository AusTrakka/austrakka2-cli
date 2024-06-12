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
        result['primitiveType'].fillna('category', inplace=True)
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
        can_visualise: str,
        column_order: int,
):
    """
    Add a field (MetaDataColumn) to AusTrakka.
    """
    fieldtype = get_fieldtype_by_name(typename)

    if can_visualise == 'viz':
        if typename in ["date", "number", "string"]:
            logger.warning(
                f"Setting colour-nodes flag on field {name} of type {typename}. "
                f"This may work poorly as colour visualisations are configured for a small "
                f"discrete set of values.")
        can_visualise = True
    elif can_visualise == 'no_viz':
        can_visualise = False
    else:
        assert can_visualise is None
        # Set visualisation behaviour based on field type
        # Here booleans and categoricals give True
        if typename == "string":
            logger.warning(
                f"Setting default of --no-colour-nodes on field {name} due to type {typename}. "
                f"If this string field should be allowed to be used for colour visualisations, "
                f"set --colour-nodes.")
        can_visualise = (typename not in ["date", "number", "string"])

    api_post(
        path=METADATACOLUMN_PATH,
        data={
            "ColumnName": name,
            "CanVisualise": can_visualise,
            "ColumnOrder": column_order,
            "MetaDataColumnTypeId": fieldtype["metaDataColumnTypeId"],
            "IsActive": True,
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
        can_visualise: str,
        column_order: int,
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
        if can_visualise == 'viz':
            if typename in ["date", "number", "string"]:
                logger.warning(
                    f"Setting colour-nodes flag on field {name} of type {typename}. "
                    f"This may work poorly as colour visualisations are configured for a "
                    f"small discrete set of values.")
        patch_fields["canVisualise"] = can_visualise == 'viz'

    if column_order is not None:
        patch_fields["columnOrder"] = column_order

    if description is not None:
        patch_fields["description"] = description

    if nndss_label is not None:
        patch_fields["nndssFieldLabel"] = nndss_label

    api_patch(
        path=f"{METADATACOLUMN_PATH}/{field['metaDataColumnId']}",
        data=patch_fields
    )
