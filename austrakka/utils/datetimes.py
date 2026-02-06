import pandas as pd
from datetime import datetime
from loguru import logger

ORIGINAL_TIMEZONE = 'original'
LOCAL_TIMEZONE = 'local'

DT_FORMAT_WITH_TZ = '%Y-%m-%d %H:%M:%S %Z'
DT_FORMAT_NO_TZ = '%Y-%m-%d %H:%M:%S'

def get_local_timezone():
    """Get the local timezone of the system."""
    return datetime.now().astimezone().tzinfo

def dt_format_and_convert(dt_series: pd.Series, timezone: str = None) -> pd.Series:
    """Convert a string datetime column to requested timezone if possible."""
    try:
        result = pd.to_datetime(dt_series, errors="coerce")
        # errors=coerce will convert unparseable datetimes to NaT and show values as missing.
        # This is appropriate for missing values which may be rendered as 0001-01-01, but bad if
        # we have a wrong column/format. Re-throw an exception if we could not parse anything.
        if result.isna().all() and not dt_series.isna().all():
            raise ValueError("Could not parse any datetimes in the column.")
    except Exception:
        logger.warning("Could not parse datetime column; will not format or convert timezone.")
        return dt_series
    
    if timezone is None or timezone==ORIGINAL_TIMEZONE:
        # No timezone conversion requested but original string may have tz info
        return result.dt.strftime(DT_FORMAT_WITH_TZ)
    
    if timezone == LOCAL_TIMEZONE:
        timezone = get_local_timezone()

    # For efficiency assume that all rows are the same in terms of tzinfo
    if result[0].tzinfo is None:
        # Timezone info was not in the original string; just format it and don't state tz
        return result.dt.strftime(DT_FORMAT_NO_TZ)

    result = result.dt.tz_convert(timezone)
    return result.dt.strftime(DT_FORMAT_WITH_TZ)
    
