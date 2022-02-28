from ....utils.misc import logger_wraps
from ....utils.api import call_api
from ....utils.api import post

JOB_INSTANCE_ROUTE = 'JobInstance'


@logger_wraps()
def add_job_instance(analysis_id: int, species_id: int):
    return call_api(
        method=post,
        path=JOB_INSTANCE_ROUTE,
        body={
            "analysis": {
                "analysisId": analysis_id,
                "species": [
                    {
                        "speciesId": species_id,
                        "isActive": True
                    }
                ],
                "isActive": True
            },
            "isActive": True
        }
    )
