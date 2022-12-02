"""
Helper functions for converting time units
"""


from datetime import datetime, timedelta
import pytz

import numpy as np


def current_datetime() -> datetime:
    """
    Returns the current time

    Returns
    -------
    datetime
        Current UTC time
    """
    return datetime.now(pytz.timezone("Etc/GMT-0"))


def block_number_to_datetime(start_time: datetime, block_number: float, time_between_blocks: float) -> datetime:
    """
    Converts the current block number to a datetime based on the start datetime of the simulation

    Arguments
    ---------
    start_time : datetime
        Timestamp at which the simulation started
    block_number : int
        Number of blocks since the simulation started
    time_between_blocks : float
        Number of seconds between blocks

    Returns
    -------
    datetime
        Timestamp at which the provided block number was (or will be) validated
    """
    delta_time = timedelta(seconds=block_number * time_between_blocks)
    return start_time + delta_time


def yearfrac_as_datetime(start_time: datetime, yearfrac: float) -> datetime:
    """
    Returns a yearfrac (e.g. the current market time) in datetime format

    Arguments
    ---------
    start_time : datetime
        Timestamp at which the simulation started
    yearfrac : float
        Fraction of a year since start_time to convert into datetime

    Returns
    -------
    datetime
        Timestamp for the provided start_time plus the provided yearfrac
    """

    dayfrac = yearfrac * 365
    delta_time = timedelta(days=dayfrac)
    return start_time + delta_time


def get_yearfrac_remaining(market_time: float, mint_time: float, token_duration: float) -> float:
    """
    Get the year fraction remaining on a token

    Arguments
    ---------
    market_time : float
        Time that has elapsed in the given market, in fractions of a year
    mint_time : float
        Time at which the token in question was minted, relative to market_time,
        in fractions of a year
    token_duration : float
        Total duration of the token's term, in fractions of a year

    Returns
    -------
    float
        Time left until token maturity, in fractions of a year
    """

    yearfrac_elapsed = market_time - mint_time
    time_remaining = np.maximum(token_duration - yearfrac_elapsed, 0)
    return time_remaining


def norm_days(days: float, normalizing_constant: float = 365) -> float:
    """
    Returns days normalized, with a default assumption of a year-long scale

    Arguments
    ---------
    days : float
        Amount of days to normalize
    normalizing_constant : float
        Amount of days to use as a normalization factor. Defaults to 365

    Returns
    -------
    float
        Amount of days provided, converted to fractions of a year
    """
    return days / normalizing_constant


def stretch_time(time: float, time_stretch: float = 1.0) -> float:
    """
    Returns stretched time values

    Arguments
    ---------
    time : float
        Time that needs to be stretched for calculations, in terms of the normalizing constant
    time_stretch : float
        Amount of time units (in terms of a normalizing constant) to use for stretching time, for calculations
        Defaults to 1

    Returns
    -------
    float
        Stretched time, using the provided parameters
    """
    return time / time_stretch


def unnorm_days(normed_days: float, normalizing_constant: float = 365) -> float:
    """
    Returns days from a value between 0 and 1

    Arguments
    ---------
    normed_days : float
        Normalized amount of days, according to a normalizing constant
    normalizing_constant : float
        Amount of days to use as a normalization factor. Defaults to 365

    Returns
    -------
    float
        Amount of days, calculated from the provided parameters
    """
    return normed_days * normalizing_constant


def unstretch_time(stretched_time: float, time_stretch: float = 1) -> float:
    """
    Returns unstretched time value, which should be between 0 and 1

    Arguments
    ---------
    stretched_time : float
        Time that has been stretched using the time_stretch factor
    time_stretch : float
        Amount of time units (in terms of a normalizing constant) to use for stretching time, for calculations
        Defaults to 1

    Returns
    -------
    float
        Time that was provided, unstretched but still based on the normalization factor
    """
    return stretched_time * time_stretch


def days_to_time_remaining(days_remaining: float, time_stretch: float = 1, normalizing_constant: float = 365) -> float:
    """
    Converts remaining pool length in days to normalized and stretched time
   
    Arguments
    ---------
    days_remaining : float
        Time left until term maturity, in days
    time_stretch : float
        Amount of time units (in terms of a normalizing constant) to use for stretching time, for calculations
        Defaults to 1
    normalizing_constant : float
        Amount of days to use as a normalization factor. Defaults to 365

    Returns
    -------
    float
        Time remaining until term maturity, in normalized and stretched time
    """

    normed_days_remaining = norm_days(days_remaining, normalizing_constant)
    time_remaining = stretch_time(normed_days_remaining, time_stretch)
    return time_remaining


def time_to_days_remaining(time_remaining: float, time_stretch: float = 1, normalizing_constant: float = 365) -> float:
    """
    Converts normalized and stretched time remaining in pool to days
   
    Arguments
    ---------
    time_remaining : float
        Time left until term maturity, in normalized and stretched time
    time_stretch : float
        Amount of time units (in terms of a normalizing constant) to use for stretching time, for calculations
        Defaults to 1
    normalizing_constant : float
        Amount of days to use as a normalization factor. Defaults to 365

    Returns
    -------
    float
        Time remaining until term maturity, in days
    """
    
    normed_days_remaining = unstretch_time(time_remaining, time_stretch)
    days_remaining = unnorm_days(normed_days_remaining, normalizing_constant)
    return days_remaining
