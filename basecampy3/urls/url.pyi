# -*- coding: utf-8 -*-
from typing import Any, AnyStr, Optional

import requests
from requests import Session
from six.moves.urllib_parse import urlencode
from . import util
from ._types import HTTPVerb


class URL(object):
    url: AnyStr
    method: HTTPVerb
    filepath: Optional[AnyStr]
    _headers: dict
    _params: dict

    def __init__(self, url: AnyStr, method: HTTPVerb = "GET",
                 params: Optional[dict] = None,
                 headers: Optional[dict] = None,
                 filepath: Optional[AnyStr] = None,
                 json_dict: Optional[dict] = None): ...

    @property
    def params(self) -> dict: ...

    @params.setter
    def params(self, value: Optional[dict]): ...

    @property
    def headers(self) -> dict: ...

    @headers.setter
    def headers(self, value: Optional[dict]): ...

    def request(self, session: Optional[Session] = None, **kwargs: Any):
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
