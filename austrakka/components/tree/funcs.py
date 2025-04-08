from io import BufferedReader
from austrakka.components.tree.version.funcs import add_tree_version
from austrakka.utils.api import api_post, api_patch
from austrakka.utils.api import api_put
from austrakka.utils.helpers.tree import get_tree_by_abbrev
from austrakka.utils.helpers.output import call_get_and_print
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import TREE_PATH


@logger_wraps()
def list_trees(project_abbrev: str, show_disabled: bool, out_format: str):
    call_get_and_print(
        f'{TREE_PATH}/project/{project_abbrev}?includeall={show_disabled}', out_format)


@logger_wraps()
def add_tree(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        is_active: bool,
        file: BufferedReader,
):
    api_post(
        path=TREE_PATH,
        data={
            'name': name,
            'description': description,
            'project': {
                'abbreviation': project
            },
            'isActive': is_active,
            'abbreviation': abbrev
        }
    )
    if file is not None:
        add_tree_version(file, abbrev)


@logger_wraps()
def update_tree(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        is_active: bool,
):
    tree = get_tree_by_abbrev(abbrev)

    if name is not None:
        tree['name'] = name
    if description is not None:
        tree['description'] = description
    if is_active is not None:
        tree['isActive'] = is_active
    if project is not None:
        tree['project']['abbreviation'] = project

    api_put(
        path=f'{TREE_PATH}/{abbrev}',
        data=tree
    )


@logger_wraps()
def disable_tree(abbrev: str):
    api_patch(
        path=f'{TREE_PATH}/disable/{abbrev}',
    )


@logger_wraps()
def enable_tree(abbrev: str):
    api_patch(
        path=f'{TREE_PATH}/enable/{abbrev}',
    )
