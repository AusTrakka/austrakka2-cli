from ....utils.misc import logger_wraps
from ....utils.api import call_api
from ....utils.api import post
from ....utils.paths import JOB_INSTANCE_PATH


@logger_wraps()
def add_job_instance(analysis_abbrev: str):
    return call_api(
        method=post,
        path=JOB_INSTANCE_PATH,
        body={
            "analysis": {
                "abbreviation": analysis_abbrev,
            }
        }
    )
