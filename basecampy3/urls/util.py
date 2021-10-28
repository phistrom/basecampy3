# -*- coding: utf-8 -*-
"""
"""

import logging as _logging
from datetime import date, datetime

import pytz
from tzlocal import get_localzone

_logger = _logging.getLogger(__name__)


def boolparam(param):
    """
    The format for boolean (True/False) parameters in Basecamp API query string
    parameters needs to be all lowercase "true" or "false". Python's "True" and
    "False" are unacceptable. This function quietly converts booleans to
    "true" or "false".

    If a parameter given is `None` or an empty string, this function returns
    `None` (so it can be filtered out of the query string).

    :param param: a parameter to coerce to Basecamp's expected boolean values
    :type param: str|bool|None
    :return: "true", "false", or `None`
    :rtype: str|None
    """
    if param is None or param == "":
        return None
    if param is True:
        return "true"
    if param is False:
        return "false"
    try:
        lower = param.strip().lower()
        if lower in ("true", "false"):
            return lower
    except AttributeError:
        pass  # wasn't a string then

    raise ValueError("Cannot determine what boolean value '%s' should have." % param)


def filter_unused(params):
    """
    Given a dictionary, remove the keys where the value is `None`.

    :param params: a dictionary to be modified
    :type params: dict|None
    """
    if params is None:
        return None
    return {k: v for k, v in params.items() if v is not None}


def fix_naive_datetime(dt, warn=True):
    """
    Given a datetime object, set its timezone to the user's local timezone.
    If given a datetime that already has timezone information, this returns
    the same timezone with no modification.

    Note that this only sets the local timezone on the given datetime object,
    it does not adjust the date and time in any way (it uses `.localize()` not
    `.astimezone()`). Also bear in mind that datetimes are immutable like
    strings. This function cannot modify the datetime you give it.

    :param dt: a datetime object to apply a timezone to
    :type dt: datetime
    :param warn: if True, emit a warning when a naive datetime is given
    :type warn: bool
    :return: a new datetime with the user's local timezone applied to it (or
             if the datetime already had a timezone, the exact same timezone
             is returned)
    :rtype: datetime
    """
    if dt.tzinfo is None:
        local_timezone = get_localzone()
        if warn:
            _logger.warning("Naive (no timezone) datetime is being converted to "
                            "'%s'." % local_timezone)
        dt = local_timezone.localize(dt)
    return dt


def to_date_string(d):
    """
    Accepts:
      * a string formatted `"%Y-%m-%d"`, in which case no conversion will be
        performed
      * a datetime object (naive datetimes will be treated as the local
        timezone and then converted to UTC before returning the date)
      * an actual date object (no timezone manipulation will be performed)
      * `None`, in which case `None` is returned

    :param d: a date-like object to convert to a date
    :type d: date|datetime|str
    :return: a string formatted "%Y-%m-%d" or None if d was None
    :rtype: str|None
    """
    if d is None:
        return None
    try:
        d.upper()  # is this a string?
        datetime.strptime(d, "%Y-%m-%d")  # raise error if bad format
        return d
    except AttributeError:
        pass  # wasn't a string
    try:
        d.date()  # is this a datetime?
        # set timezone to UTC and return date
        dt = fix_naive_datetime(d)  # warn if naive
        dt = dt.astimezone(pytz.utc)
        return dt.strftime("%Y-%m-%d")
    except AttributeError:
        pass  # wasn't a datetime
    try:
        int(d.year)  # is it a date object?
        return d.strftime("%Y-%m-%d")
    except AttributeError:
        # it was not a date object
        raise ValueError("No idea how to convert %s of type '%s' to a date." %
                         (d, type(d).__name__))


def to_ids(iterable):
    """
    Given an iterable of integers and/or Basecampy objects with an `id`
    parameter, converts the iterable to be entirely integers (converting the
    Basecampy objects to their `id`s and not touching the existing integers.

    If `iterable` is `None`, returns `None`.

    :param iterable: an iterable of integers and/or Basecampy objects
    :type iterable: list[basecampy3.endpoints._base.BasecampObject|dict|int]
    :return: all elements of the iterable converted to integers
    :rtype: list[int]
    """
    if iterable is None:
        return None
    ids = []
    for i in iterable:
        try:
            _id = int(getattr(i, "id", i))
        except TypeError:
            _id = int(dict.get(i, "id", i))
        ids.append(_id)
    return ids
