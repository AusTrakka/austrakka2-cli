from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.api import put
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.paths import JOB_DEFINITION_PATH
from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.definition import get_definition_by_name


@logger_wraps()
def list_definitions(out_format: str):
    call_get_and_print_table(JOB_DEFINITION_PATH, out_format)


@logger_wraps()
def add_definition(
        name: str,
        description: str,
        is_active: bool
):
    call_api(
        method=post,
        path=JOB_DEFINITION_PATH,
        body={
            "name": name,
            "description": description,
            "isActive": is_active,
            "unavailable": True,
        }
    )


@logger_wraps()
def update_definition(
        name: str,
        description: str,
        is_active: bool
):
    definition = get_definition_by_name(name)

    if description is not None:
        definition['description'] = description

    if is_active is not None:
        definition['isActive'] = is_active

    call_api(
        method=put,
        path=f'{JOB_DEFINITION_PATH}/{definition["jobDefinitionId"]}',
        body=definition
    )
