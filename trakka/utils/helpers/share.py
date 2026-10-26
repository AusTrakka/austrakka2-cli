from typing import List   

def resolve_share_targets(group_names: List[str] = None, projects: List[str] = None):
    if not group_names and not projects:
        raise ValueError(
            "Either Group Name(s) or Project(s) must be provided to share")

    if group_names and projects:
        raise ValueError(
            "Group Name(s) and Project(s) cannot both be provided to share.")
        
    if projects:
        return [project+'-Group' for project in projects]
    
    return group_names
