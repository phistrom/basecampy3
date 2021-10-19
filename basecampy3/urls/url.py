# -*- coding: utf-8 -*-
"""
URL class definition module. URLs are used to more easily make requests to the
Basecamp 3 API.
"""

import requests
from six.moves.urllib_parse import urlencode
from . import util


class URL(object):
    """
    Grouping of a URL string, an HTTP verb, and other optional parameters that
    may be needed to interact with a single endpoint of the Basecamp 3 API.
    """

    def __init__(self, url, method="GET", params=None, headers=None, filepath=None, json_dict=None):
        """
        :param url: the full URL as a string
        :type url: typing.AnyStr
        :param method: the HTTP verb to use (GET, POST, PUT, DELETE, etc.)
        :type method: typing.AnyStr
        :param params: a query string (?key1=val1&key2=val2...) as a dictionary
        :type params: dict
        :param headers: additional headers to include with this request
        :type headers: dict
        :param filepath: path to a file to use as content for the request body
        :type filepath: typing.AnyStr
        :param json_dict: a dictionary to JSONify and use as the request body
        :type json_dict: dict
        """
        self.url = url
        self.method = method
        self._params = None
        self.params = params
        self.filepath = filepath
        self._headers = None
        self.headers = headers
        self.json_dict = json_dict

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if value is None:
            value = {}
        self._params = util.filter_unused(value)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        if value is None:
            self._headers = {}
        else:
            self._headers = value

    def request(self, session=None, **kwargs):
        """
        Perform a requests.request with the given Session object.
        This object's method and URL, as well as the kwargs you supply
        will be used to make the HTTP request.

        :param session: the Requests Session object you wish to use. Otherwise this request is a one-off.
        :type session: requests.Session|None
        :param params: optionally add query string (GET) parameters to the URL in dict format
        :type params: dict|None
        :return: the HTTP response to this HTTP request
        :rtype: requests.Response
        """
        if session is None:
            session = requests  # no session, just call it like i.e. `requests.request("GET", ...)`
        # if there's already params for this URL, update it's values with any that were
        # passed into this function
        params_to_use = self.params.copy()
        try:
            params_to_use.update(kwargs["params"])
        except KeyError:
            pass  # no extra params were given
        params_to_use = util.filter_unused(params_to_use)

        headers = self.headers.copy()
        try:
            headers.update(kwargs["headers"])
        except KeyError:
            pass  # no extra headers were given

        if self.json_dict and not kwargs.get("json"):
            kwargs["json"] = self.json_dict

        kwargs["method"] = self.method
        kwargs["url"] = self.url
        kwargs["params"] = params_to_use
        kwargs["headers"] = headers

        if self.filepath and not kwargs.get("data"):
            with open(self.filepath, "rb") as infile:
                kwargs["data"] = infile
                response = session.request(**kwargs)
        else:
            response = session.request(**kwargs)

        return response

    def __eq__(self, other):
        return self.url == other.url and self.method == other.method

    def __hash__(self):
        return hash(self.method) ^ hash(self.url)

    def __lt__(self, other):
        for attr in ["method", "url"]:
            mine = getattr(self, attr)
            theirs = getattr(other, attr)
            if mine == theirs:
                continue
            return mine < theirs
        return False

    def __repr__(self):
        return "%s %s" % (self.method, self.url)

    def __str__(self):
        if self.params:
            return "%s?%s" % (self.url, urlencode(self.params))
        else:
            return self.url
