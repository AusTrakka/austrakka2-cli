AUSTRAKKA_ADMIN = "AusTrakkaAdmin"
ORGANISATION_ADMIN = "OrganisationAdmin"
UPLOADER = "Uploader"
VIEWER = "Viewer"
CURATOR = "Curator"


def get_role_list():
    return [
        AUSTRAKKA_ADMIN,
        ORGANISATION_ADMIN,
        UPLOADER,
        VIEWER,
        CURATOR,
    ]
