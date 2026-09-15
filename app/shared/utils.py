"""
app/shared/utils/utils.py

Here i will make the utils function to use in many places easily all time
"""

import time
from datetime import datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

ind_timezone = ZoneInfo("Asia/Kolkata")


def generate_hex_uuid4() -> str:
    """
    This will generate the uuid4 with a string value
    i will use this for random data in the columns mainly in database
    """
    return str(uuid4().hex)


def current_posix_time():
    """
    This will generate the current time as of posix
    1 january 1970 as of utc
    """
    current_time_int = int(time.time())
    return current_time_int


def posix_to_readable_time(
    ts: int,
    fmt: str = "%d %b %Y, %I:%M:%S %p IST",
) -> str:
    """
    This will convert from int to str so that i can read

    I keep the fmt here so that in the template i can use this value
    to get my choice of time there in the html i can do,

    {{ category.created_time | read_posix_time_fun("%d/%m/%Y") }}

    """
    if not ts:
        return ""

    time = datetime.fromtimestamp(
        timestamp=ts,
        tz=ind_timezone,
    )
    time_str = time.strftime(
        format=fmt,
    )

    return time_str
