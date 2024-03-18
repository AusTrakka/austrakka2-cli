from austrakka.utils.api import api_post
from austrakka.utils.api import api_put
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.paths import JOB_DEFINITION_PATH
from austrakka.utils.misc import logger_wraps
from austrakka.utils.helpers.definition import get_definition_by_name


@logger_wraps()
def list_definitions(out_format: str):
    call_get_and_print(JOB_DEFINITION_PATH, out_format)


@logger_wraps()
def add_definition(
        name: str,
        description: str,
        is_active: bool
):
    api_post(
        path=JOB_DEFINITION_PATH,
        data={
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

    api_put(
        path=f'{JOB_DEFINITION_PATH}/{name}',
        data=definition
    )
