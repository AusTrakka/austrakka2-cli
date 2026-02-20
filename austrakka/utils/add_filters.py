def add_equals_filter(filters: dict, field: str, value):
    if value is not None:
        filters[field] = {
            "operator": "and",
            "constraints": [
                {
                    "value": value,
                    "matchMode": "equals"
                }
            ]
        }
