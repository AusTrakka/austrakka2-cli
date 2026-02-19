from datetime import datetime
import dateparser
from loguru import logger
import pandas as pd

from austrakka.utils.misc import logger_wraps
from austrakka.utils.context import AusTrakkaCxt, CxtKey

ORIGINAL_TIMEZONE = 'original'
LOCAL_TIMEZONE = 'local'

API_DATETIME_FORMAT = 'ISO8601'
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
        result = pd.to_datetime(dt_series, errors="coerce", format=API_DATETIME_FORMAT)
    except ValueError:
        logger.warning(
            f"Could not parse datetime column {dt_series.name}; "
            "will not format or convert timezone.")
        return dt_series
    
    timezone_str = AusTrakkaCxt.get_value(CxtKey.TIMEZONE)
    if timezone_str==ORIGINAL_TIMEZONE:
        # No timezone conversion requested but original string may have tz info
        return result.dt.strftime(DT_FORMAT_WITH_TZ)
    
    timezone = parse_timezone(timezone_str)

    if result.dt.tz is None:
        # Timezone info was not in the original string; just format it and don't state tz
        return result.dt.strftime(DT_FORMAT_NO_TZ)

    result = result.dt.tz_convert(timezone)
    return result.dt.strftime(DT_FORMAT_WITH_TZ)

# This is generally used for parsing user input where the format can vary.
# Datetimes supplied by the server are in ISO8601 format and can be parsed as above
def dt_parse(datestr: str):
    """
    Parse a single datetime string. 
    If the string does not contain timezone info, it will be treated as the specified timezone.
    If the string contains timezone info, this overrides the specified timezone.
    """
    dt = dateparser.parse(datestr)
    if dt is None:
        raise ValueError(f"Could not parse datetime string: {datestr}")
    if not dt.tzinfo:
        timezone = parse_timezone()
        dt = dt.replace(tzinfo=timezone)
    return dt
