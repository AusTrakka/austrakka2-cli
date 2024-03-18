import pandas as pd

from loguru import logger

from austrakka.utils.helpers.fieldtype import get_fieldtype_by_name
from austrakka.utils.helpers.fields import get_field_by_name
from austrakka.utils.api import api_get
from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.misc import logger_wraps
from austrakka.utils.output import print_formatted
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

    if 'mappedSpecies' in result:
        result.drop(['mappedSpecies'],
                    axis='columns',
                    inplace=True)
    if 'primitiveType' in result:
        result['primitiveType'].fillna('category', inplace=True)

    print_formatted(
        result,
        out_format,
    )


@logger_wraps()
def add_field(
        name: str,
        typename: str,
        can_visualise: str,
        column_order: int,
        show_at_start: bool,
        min_width: int,
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
            "IsDisplayedAsDefault": show_at_start,
            "MetaDataColumnTypeId": fieldtype["metaDataColumnTypeId"],
            "IsActive": True,
            "MinWidth": min_width,
        }
    )


@logger_wraps()
def update_field(
        name: str,
        new_name: str,
        typename: str,
        can_visualise: str,
        column_order: int,
        set_show: str,
        min_width: int,
):
    """
    Update a field (MetaDataColumn) within AusTrakka.

    name specifies the name of the field to modify. All other parameters are optional, and their
    corresponding values will only be updated if they are specified.
    """
    field = get_field_by_name(name)

    put_field = {k: field[k] for k in [
        "columnName",
        "canVisualise",
        "columnOrder",
        "isDisplayedAsDefault",
        "isActive",
        "metaDataColumnTypeId",
        "minWidth",
    ]}

    if new_name is not None:
        logger.warning(f"Updating field name from {name} to {new_name}")
        put_field["columnName"] = new_name

    if typename is not None:
        fieldtype = get_fieldtype_by_name(typename)
        put_field["metaDataColumnTypeId"] = fieldtype["metaDataColumnTypeId"]

    if can_visualise is not None:
        if can_visualise == 'viz':
            if typename in ["date", "number", "string"]:
                logger.warning(
                    f"Setting colour-nodes flag on field {name} of type {typename}. "
                    f"This may work poorly as colour visualisations are configured for a "
                    f"small discrete set of values.")
        put_field["canVisualise"] = can_visualise == 'viz'

    if column_order is not None:
        put_field["columnOrder"] = column_order

    if set_show is not None:
        put_field["isDisplayedAsDefault"] = set_show == 'show'

    if min_width is not None:
        put_field["minWidth"] = min_width

    api_put(
        path=f"{METADATACOLUMN_PATH}/{field['metaDataColumnId']}",
        data=put_field
    )
