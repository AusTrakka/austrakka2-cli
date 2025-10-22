from austrakka.utils.paths import ORG_V2_PATH, TENANT_PATH

TENANT_RESOURCE = 'Tenant'
ORG_RESOURCE = 'Organisation'


def convert_record_type_to_route_string(record_type):
    record_type_route = record_type
    if record_type == ORG_RESOURCE:
        record_type_route = ORG_V2_PATH
    return record_type_route


def get_priv_path(record_type: str, record_global_id: str):
    if record_type == TENANT_RESOURCE:
        return TENANT_PATH
    return f'{record_type}/{record_global_id}'
