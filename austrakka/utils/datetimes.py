from datetime import datetime
import dateparser
from loguru import logger
import pandas as pd

from austrakka.utils.misc import logger_wraps
from austrakka.utils.context import AusTrakkaCxt, CxtKey

ORIGINAL_TIMEZONE = 'original'
LOCAL_TIMEZONE = 'local'

DT_FORMAT_WITH_TZ = '%Y-%m-%d %H:%M:%S %Z'
DT_FORMAT_NO_TZ = '%Y-%m-%d %H:%M:%S'

def parse_timezone(timezone_str: str = None):
    """
    Parse a timezone string to interpret special values such as "local".
    Returns a timezone object.
    If timezone_str is None, will get the current context value.
    """
    if timezone_str is None:
        timezone_str = AusTrakkaCxt.get_value(CxtKey.TIMEZONE)
    
    if timezone_str.lower() == LOCAL_TIMEZONE:
        return datetime.now().astimezone().tzinfo
    
    # If this function is called it means we want to do timezone conversion, 
    # so if set to "original" we use local timezone in order to "not convert"
    # "original" will leave both server datetimes and user-supplied datetimes untouched
    if timezone_str.lower() == ORIGINAL_TIMEZONE:
        return datetime.now().astimezone().tzinfo
    
    timezone = dateparser.parse(f"now in {timezone_str}").tzinfo
    if timezone is None:
        raise ValueError(f"Could not parse timezone string: {timezone_str}")
    return timezone
  

@logger_wraps()
def dt_format_and_convert(dt_series: pd.Series) -> pd.Series:
    """Convert a string datetime column to requested timezone if possible."""
    try:
        result = pd.to_datetime(dt_series, errors="coerce")
        # errors=coerce will convert unparseable datetimes to NaT and show values as missing.
        # This is appropriate for missing values which may be rendered as 0001-01-01, but bad if
        # we have a wrong column/format. Re-throw an exception if we could not parse anything.
        if result.isna().all() and not dt_series.isna().all():
            raise ValueError("Could not parse any datetimes in the column.")
    except ValueError:
        logger.warning("Could not parse datetime column; will not format or convert timezone.")
        return dt_series
    
    timezone_str = AusTrakkaCxt.get_value(CxtKey.TIMEZONE)
    if timezone_str==ORIGINAL_TIMEZONE:
        # No timezone conversion requested but original string may have tz info
        return result.dt.strftime(DT_FORMAT_WITH_TZ)
    
    timezone = parse_timezone(timezone_str)

    # For efficiency assume that all rows are the same in terms of tzinfo
    if result[0].tzinfo is None:
        # Timezone info was not in the original string; just format it and don't state tz
        return result.dt.strftime(DT_FORMAT_NO_TZ)

    result = result.dt.tz_convert(timezone)
    return result.dt.strftime(DT_FORMAT_WITH_TZ)

def dt_parse(input: str):
    """
    Parse a single datetime string. 
    If the string does not contain timezone info, it will be treated as the specified timezone.
    If the string contains timezone info, this overrides the specified timezone.
    """
    dt = dateparser.parse(input)
    if dt is None:
        raise ValueError(f"Could not parse datetime string: {input}")
    if not dt.tzinfo:
        timezone = parse_timezone()
        dt = dt.replace(tzinfo=timezone)
    return dt
    