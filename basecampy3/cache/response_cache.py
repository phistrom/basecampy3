import abc
import six


@six.add_metaclass(abc.ABCMeta)
class ResponseCache(object):
    """
    Extend this class to create your own caching for Basecamp 3 API calls. The responsibility of the cache is to
    remember the ETag and Last-Modified headers returned by a call and send it on a subsequent call. Basecamp 3 will
    respond with a "304 Not Modified" and no content if the response would be the same as last time. Then you can just
    return the cached Response.

    requests.Response objects can be Pickled, so they can be stored externally like in Redis, a file, or a database.
    """

    @abc.abstractmethod
    def get_cached_headers(self, method, url):
        """
        Given a request, gets the cached headers if we've seen this exact request METHOD and URL before.
        The headers will be given in the form of tuple(ETAG, LAST_MODIFIED).
        :param method: the HTTP method in all caps (i.e. 'GET', 'POST', 'PUT')
        :type method: str
        :param url: the URL of the request
        :type url: str
        :return: the headers as a 2-element tuple. One or both can be `None` if the headers have not been cached before.
        :rtype: tuple(str)
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_cached_response(self, method, url):
        """
        Get a requests.Response object that was cached. The key is the METHOD and URL.

        :param method: the HTTP method in all caps (i.e. 'GET', 'POST', 'PUT')
        :type method: str
        :param url: the URL of the request
        :type url: str
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
