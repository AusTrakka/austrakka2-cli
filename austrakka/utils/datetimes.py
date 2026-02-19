from datetime import datetime
from loguru import logger

import pandas as pd

ORIGINAL_TIMEZONE = 'original'
LOCAL_TIMEZONE = 'local'

API_DATETIME_FORMAT = 'ISO8601'
DT_FORMAT_WITH_TZ = '%Y-%m-%d %H:%M:%S %Z'
DT_FORMAT_NO_TZ = '%Y-%m-%d %H:%M:%S'

def get_local_timezone():
    """Get the local timezone of the system."""
    return datetime.now().astimezone().tzinfo

def dt_format_and_convert(dt_series: pd.Series, timezone: str = None) -> pd.Series:
    """Convert a string datetime column to requested timezone if possible."""
    try:
        result = pd.to_datetime(dt_series, errors="coerce", format=API_DATETIME_FORMAT)
    except ValueError:
        logger.warning(
            f"Could not parse datetime column {dt_series.name}; "
            "will not format or convert timezone.")
        return dt_series
    
    if timezone is None or timezone==ORIGINAL_TIMEZONE:
        # No timezone conversion requested but original string may have tz info
        return result.dt.strftime(DT_FORMAT_WITH_TZ)
    
    if timezone == LOCAL_TIMEZONE:
        timezone = get_local_timezone()

    if result.dt.tz is None:
        # Timezone info was not in the original string; just format it and don't state tz
        return result.dt.strftime(DT_FORMAT_NO_TZ)

    result = result.dt.tz_convert(timezone)
    return result.dt.strftime(DT_FORMAT_WITH_TZ)
