# -*- coding: utf-8 -*-
"""
"""


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
