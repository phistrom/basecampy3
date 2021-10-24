import abc

import six
from six.moves.urllib_parse import parse_qsl, urlparse

from .. import exc


@six.add_metaclass(abc.ABCMeta)
class ResponseCache(object):
    """
    Extend this class to create your own caching for Basecamp 3 API calls. The responsibility of the cache is to
    remember the ETag and Last-Modified headers returned by a call and send it on a subsequent call. Basecamp 3 will
    respond with a "304 Not Modified" and no content if the response would be the same as last time. Then you can just
    return the cached Response.

    requests.Response objects can be Pickled, so they can be stored externally like in Redis, a file, or a database.
    """

    @staticmethod
    def _request_to_hash(request):
        """
        The PreparedRequest object in Python requests is not hashable. This
        function attempts to generate a hash that will be equal between two
        PreparedRequest objects if their method, URL, query-strings, and body
        match.

        :param request: a Request object to hash
        :type request: requests.PreparedRequest
        :return: a version of the PreparedRequest object that can be hashed
        :rtype: int
        """
        parsed = urlparse(request.url)

        url = parsed.geturl()  # the URL without the query-string

        # sort the querysting parameters into a tuple of 2-element tuples
        # i.e. ?key2=val2&key1=val1 becomes ((key1, val1), (key2, val2))
        querystring = tuple(sorted(parse_qsl(parsed.query)))

        # if body is None, use an empty string instead

        body = ResponseCache._body_to_hashable(request)

        key = (request.method, url, querystring, body)
        hashed = hash(key)
        return hashed

    @staticmethod
    def _body_to_hashable(request):
        body = request.body if request.body else b""
        try:
            len(body)  # raise TypeError if not string/bytes
            if hasattr(body, "upper"):
                return body
        except TypeError:
            pass
        try:
            # this gets the file name if it's a BufferedReader
            return body.raw.name
        except AttributeError:
            pass
        raise exc.UnhashableError("Unable to hash request.body")

    @abc.abstractmethod
    def get_cached_headers(self, request):
        """
        Given a request, gets the cached headers if we've seen it before.
        The headers will be given in the form of tuple(ETAG, LAST_MODIFIED).

        :param request: a Request object
        :type request: requests.PreparedRequest
        :return: the headers as a 2-element tuple. One or both can be `None` if the headers have not been cached before.
        :rtype: tuple(str)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_cached_response(self, request):
        """
        Get a requests.Response object that was cached. The key is the METHOD and URL.

        :param request: a Request object
        :type request: requests.PreparedRequest
        :return: the Response object that has been cached since the last time this endpoint was called
        :rtype: requests.Response
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def set_cached(self, response):
        """
        Cache this Response object.

        :param response: the Response object from a successful call to be retrieved later
        :type response: requests.Response
        """
        raise NotImplementedError()
