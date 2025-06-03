"""
Date helper utility functions for the pythontest project.
Provides common date formatting and manipulation functions.
"""
import datetime
from typing import Optional, Union


def format_iso_date(date_obj: Optional[Union[datetime.datetime, datetime.date]] = None) -> str:
    """
    Format a date object to ISO 8601 format (YYYY-MM-DD).
    If no date is provided, uses the current date.
    
    Args:
        date_obj: The date object to format. Defaults to current date if None.
        
    Returns:
        String representation of the date in ISO format.
    """
    if date_obj is None:
        date_obj = datetime.datetime.now()
    
    if isinstance(date_obj, datetime.datetime):
        return date_obj.date().isoformat()
    return date_obj.isoformat()


def get_date_range(days: int) -> tuple[datetime.date, datetime.date]:
    """
    Get a date range from today to N days ago.
    
    Args:
        days: Number of days to go back
        
    Returns:
        Tuple of (start_date, end_date) where end_date is today
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    return start_date, end_date


def is_weekend(date_obj: Optional[Union[datetime.datetime, datetime.date]] = None) -> bool:
    """
    Check if the given date is a weekend (Saturday or Sunday).
    If no date is provided, uses the current date.
    
    Args:
        date_obj: The date object to check. Defaults to current date if None.
        
    Returns:
        True if the date is a weekend, False otherwise.
    """
    if date_obj is None:
        date_obj = datetime.datetime.now()
    
    # 5 = Saturday, 6 = Sunday
    return date_obj.weekday() >= 5