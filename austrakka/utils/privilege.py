
def convert_record_type_to_route_string(record_type):
    record_type_route = record_type
    if record_type == 'Organisation':
        record_type_route = "OrganisationV2"
    elif record_type == 'ProForma':
        record_type_route = "ProFormaV2"
    elif record_type == 'Project':
        record_type_route = "ProjectV2"
    return record_type_route
    