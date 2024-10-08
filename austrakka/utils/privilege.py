
def convert_record_type_to_route_string(record_type):
    record_type_route = record_type
    if record_type == 'Organisation':
        record_type_route = "OrganisationV2"
    return record_type_route
    