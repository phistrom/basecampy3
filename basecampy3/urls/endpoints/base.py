# -*- coding: utf-8 -*-
"""
Base class for other groupings of URLs in the API.
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
        """
        The base portion of the URL to access Basecamp 3 API.
        This is usually https://3.basecampapi.com/{YourAccountID}.

        :param base_url: the prefix to all the URIs in this object
        :type base_url: typing.AnyStr
        """
        self._base_url = None
        self.base_url = base_url

    @property
    def base_url(self):
        """
        The prefix to all the URIs in this object.
        :rtype: typing.AnyStr
        """
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        """
        :type value: typing.AnyStr
        """
        value = value.rstrip("/")
        self._base_url = value

    def _delete(self, uri, **kwargs):
        """
        Convenience method for _make_url("DELETE", ...)
        """
        return self._make_url(DELETE, uri, **kwargs)

    def _get(self, uri, **kwargs):
        """
        Convenience method for _make_url("GET", ...)
        """
        return self._make_url(GET, uri, **kwargs)

    def _post(self, uri, **kwargs):
        """
        Convenience method for _make_url("POST", ...)
        """
        return self._make_url(POST, uri, **kwargs)

    def _put(self, uri, **kwargs):
        """
        Convenience method for _make_url("PUT", ...)
        """
        return self._make_url(PUT, uri, **kwargs)

    def _make_url(self, method, uri, params=None, headers=None, filepath=None, json_dict=None, **kwargs):
        """
        Create a new URL object with the given parameters. `kwargs` are used to
        `.format()` the `uri` parameter. `kwargs` can be either integers
        (the ID of a Basecamp object), or they can be `BasecampObject`s.

        :param method: the HTTP verb (GET, POST, etc.)
        :type method: typing.AnyStr
        :param uri: the URI path to append to the `base_url`
        :type uri: typing.AnyStr
        :param params: query string parameters as a dictionary
        :type params: dict|None
        :param headers: HTTP headers as a dictionary
        :type headers: dict|None
        :param filepath: the path to a file to use as contents for a request body
        :type filepath: typing.AnyStr
        :param json_dict: a dictionary to JSONify and use as the request body
        :type json_dict: dict
        :param kwargs: used to replace the placeholders in the URI
        :type kwargs: typing.AnyStr|basecampy3.endpoints._base.BasecampObject
        :return: a URL that can be used to make requests to the API
        :rtype: basecampy3.urls.URL
        """
        # replace any BasecampObjects in kwargs values with their `id` instead
        if uri.startswith("/"):
            uri = uri[1:]
        kwargs = {k: getattr(v, "id", v) for k, v in kwargs.items()}
        urlstring = "/".join((self._base_url, uri))
        urlstring = urlstring.format(**kwargs)
        return URL(url=urlstring, method=method, params=params,
                   headers=headers, filepath=filepath, json_dict=json_dict)
