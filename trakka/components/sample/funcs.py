from trakka.utils.misc import logger_wraps
from trakka.utils.api import api_patch
from trakka.utils.paths import SAMPLE_PATH, DETAILS_PATH
from trakka.utils.paths import ORG_PATH
from trakka.utils.helpers.output import call_get_and_print

DISABLE = 'Disable'
ENABLE = 'Enable'
UNSHARE = 'UnShare'
SHARE = 'Share'
PROJECTS = 'Projects'
PURGE = 'Purge'
SAMPLES_OWNER = 'samplesOwner'

@logger_wraps()
def change_owner(curr_org: str, new_org: str, seq_ids: [str]):
    api_patch(
        path=f"{ORG_PATH}/{curr_org}/{SAMPLES_OWNER}",
        data={
            "seqIds": seq_ids,
            "newOwnerAbbrev": new_org
        },
    )

@logger_wraps()
def show_sample(
        seq_id: str,
        out_format: str,
):
    call_get_and_print(
        path="/".join([SAMPLE_PATH, seq_id]),
        out_format=out_format
    )

@logger_wraps()
def show_sample_details(
        seq_id: str,
        out_format: str,
):
    call_get_and_print(
        path="/".join([SAMPLE_PATH, seq_id, DETAILS_PATH]),
        out_format=out_format
    )

@logger_wraps()
def share_sample(
        project: str = None,
        seq_ids: [str] = None,
):
    api_patch(
        path="/".join([SAMPLE_PATH, SHARE]),
        data={
            "seqIds": seq_ids,
            "projectIdentifier": project
        },
    )


@logger_wraps()
def unshare_sample(
        project: str = None,
        seq_ids: [str] = None,
):
    api_patch(
        path="/".join([SAMPLE_PATH, UNSHARE]),
        data={
            "seqIds": seq_ids,
            "projectIdentifier": project
        },
    )


@logger_wraps()
def get_sample_projects(
        seq_id: str,
        out_format
):
    call_get_and_print(
        path=f"{SAMPLE_PATH}/{seq_id}/{PROJECTS}",
        out_format=out_format
    )

@logger_wraps()
def disable_sample(
        seq_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, DISABLE]),
        data={
            "seqIds": seq_ids
        },
    )


@logger_wraps()
def enable_sample(
        seq_ids: [str]
):
    api_patch(
        path="/".join([SAMPLE_PATH, ENABLE]),
        data={
            "seqIds": seq_ids
        },
    )


@logger_wraps()
def purge_sample(
        seq_id: str
):
    api_patch(
        path="/".join([SAMPLE_PATH, seq_id, PURGE]),
    )
