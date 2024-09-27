from datetime import datetime
from typing import Tuple

def get_year_and_month(from_ms: int) -> Tuple[int, int]:
    """
    Get the year and month from a given Unix milliseconds timestamp.

    Args:
        from_ms (int): Unix milliseconds timestamp.

    Returns:
        Tuple[int, int]: Year and month.
    """
    # Convert from_ms to a datetime object
    dt = datetime.fromtimestamp(from_ms / 1000)

    # Extract year and month
    year = dt.year
    month = dt.month

    return year, month