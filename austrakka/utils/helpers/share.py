def resolve_share_target(group_name: str = None, project: str = None,):
    if group_name is None and project is None:
        raise ValueError(
            "Either Group Name or Project must be provided to share sequences")

    if group_name is None and project is not None:
        group_name = project+'-Group' 
        
    return group_name
    