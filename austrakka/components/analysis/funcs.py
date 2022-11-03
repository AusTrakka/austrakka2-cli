from austrakka.utils.helpers.analysis import get_analysis_by_abbrev
from austrakka.utils.misc import logger_wraps
from austrakka.utils.paths import ANALYSIS_PATH
from austrakka.utils.helpers.output import call_get_and_print_table
from austrakka.utils.api import call_api
from austrakka.utils.api import post
from austrakka.utils.api import put


@logger_wraps()
def list_analyses(out_format: str):
    call_get_and_print_table(ANALYSIS_PATH, out_format)


@logger_wraps()
def add_analysis(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        definition_abbrev: str,
        filter_str: str,
        is_active: bool,
):
    call_api(
        method=post,
        path=ANALYSIS_PATH,
        body={
            'name': name,
            'description': description,
            'jobDefinition': {
                'id': definition_abbrev
            },
            'project': {
                'abbreviation': project
            },
            'filterString': filter_str,
            'isActive': is_active,
            'abbreviation': abbrev
        }
    )


@logger_wraps()
def update_analysis(
        abbrev: str,
        name: str,
        description: str,
        project: str,
        definition_abbrev: str,
        filter_str: str,
        is_active: bool,
):
    analysis = get_analysis_by_abbrev(abbrev)

    if name is not None:
        analysis['name'] = name
    if description is not None:
        analysis['description'] = description
    if filter_str is not None:
        analysis['filterString'] = filter_str
    if is_active is not None:
        analysis['isActive'] = is_active
    if project is not None:
        analysis['project']['abbreviation'] = project
    if definition_abbrev is not None:
        analysis['jobDefinition']['id'] = definition_abbrev

    call_api(
        method=put,
        path=f'{ANALYSIS_PATH}/{abbrev}',
        body=analysis
    )
