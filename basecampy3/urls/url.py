# -*- coding: utf-8 -*-
"""
"""

import requests
from six.moves.urllib_parse import urlencode
from . import util


class URL(object):
    def __init__(self, url, method="GET", params=None):
        self.url = url
        self.method = method
        self._params = None
        self.params = params

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        if value is None:
            value = {}
        self._params = util.filter_unused(value)

    def request(self, session=None, params=None, **kwargs):
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
        if params is None:
            params = {}
        params_to_use.update(params)
        params_to_use = util.filter_unused(params_to_use)
        response = session.request(method=self.method, url=self.url, params=params_to_use, **kwargs)
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
