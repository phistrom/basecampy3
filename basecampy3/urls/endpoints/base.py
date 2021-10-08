# -*- coding: utf-8 -*-
"""
"""

import abc
import logging
import six
from ..url import URL


logger = logging.getLogger(__name__)

DELETE = "DELETE"
GET = "GET"
POST = "POST"
PUT = "PUT"


@six.add_metaclass(abc.ABCMeta)
class EndpointURLs(object):
    def __init__(self, base_url):
        self._base_url = base_url

    def _delete(self, uri, **kwargs):
        return self._make_url(DELETE, uri, **kwargs)

    def _get(self, uri, **kwargs):
        return self._make_url(GET, uri, **kwargs)

    def _post(self, uri, **kwargs):
        return self._make_url(POST, uri, **kwargs)

    def _put(self, uri, **kwargs):
        return self._make_url(PUT, uri, **kwargs)

    def _make_url(self, method, uri, params=None, **kwargs):
        # replace any BasecampObjects in kwargs values with their `id` instead
        if uri.startswith("/"):
            uri = uri[1:]
        kwargs = {k: getattr(v, "id", v) for k, v in kwargs.items()}
        urlstring = "/".join((self._base_url, uri))
        urlstring = urlstring.format(**kwargs)
        return URL(urlstring, method, params)
