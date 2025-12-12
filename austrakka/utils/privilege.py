from austrakka.utils.paths import ORG_V2_PATH
from austrakka.utils.paths import PROFORMA_V2_PATH
from austrakka.utils.paths import PROJECT_V2_PATH
from austrakka.utils.paths import TENANT_PATH
from austrakka.utils.paths import USER_V2_PATH

TENANT_RESOURCE = 'Tenant'
ORG_RESOURCE = 'Organisation'
PROJECT_RESOURCE = 'Project'
PROFORMA_RESOURCE = 'Proforma'
USER_RESOURCE = 'User'


def _convert_record_type_to_route_string(record_type):
    record_type_route = record_type
    if record_type == ORG_RESOURCE:
        record_type_route = ORG_V2_PATH
    if record_type == PROJECT_RESOURCE:
        record_type_route = PROJECT_V2_PATH
    if record_type == PROFORMA_RESOURCE:
        record_type_route = PROFORMA_V2_PATH
    if record_type == USER_RESOURCE:
        record_type_route = USER_V2_PATH
    return record_type_route


def get_priv_path(record_type: str, record_global_id: str):
    if record_type == TENANT_RESOURCE:
        return TENANT_PATH
    return f'{_convert_record_type_to_route_string(record_type)}/{record_global_id}'
