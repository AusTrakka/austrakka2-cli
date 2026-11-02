# pylint: disable=R0801

from trakka.utils.helpers.output import call_get_and_print
from trakka.utils.misc import logger_wraps
from trakka.utils.paths import PROJECT_PATH

@logger_wraps()
def download_view(
        abbrev: str,
        out_format: str
):
    path = "/".join([PROJECT_PATH, abbrev, "download-project-view"])
    call_get_and_print(path, out_format)
