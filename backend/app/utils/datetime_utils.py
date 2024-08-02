from datetime import datetime


def remove_timezone(dt: datetime) -> datetime:
    """Convert timezone-aware datetime to timezone-naive datetime."""
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt
