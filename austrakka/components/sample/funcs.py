from austrakka.utils.misc import logger_wraps
from austrakka.utils.api import call_api
from austrakka.utils.api import patch
from austrakka.utils.paths import SAMPLE_PATH

DISABLE = 'Disable'


@logger_wraps()
def disable_sample(
        sample_ids: [str]
):
    call_api(
        method=patch,
        path="/".join([SAMPLE_PATH, DISABLE]),
        body={
            "seqIds": sample_ids
        },
    )
