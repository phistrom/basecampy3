from requests import adapters
from .constants import RATE_LIMIT_PER_SECONDS, RATE_LIMIT_REQUESTS
from .log import logger
from .cache import DictionaryCache
from .rated_semaphore import RatedSemaphore


class Basecamp3TransportAdapter(adapters.HTTPAdapter):
    """
    Handles API request caching and rate-limiting.
    """

    SEMAPHORE = RatedSemaphore(RATE_LIMIT_REQUESTS, RATE_LIMIT_PER_SECONDS)
    """
    Used to keep us under the limits defined here 
    https://github.com/basecamp/bc3-api#rate-limiting-429-too-many-requests
    A `RatedSemaphore` allows us to block if we hit the API limits.
    """

    def __init__(self, cache_backend=None, *args, **kwargs):
        """
        Applied to a requests.Session object to implement caching and rate-limiting

        :param cache_backend: stores responses for later retrieval if the response is unchanged
        :type cache_backend: basecampy3.response_cache.ResponseCache
        :param args: whatever args are supported by requests.adapters.HTTPAdapter
        :param kwargs: whatever kwargs are supported by requests.adapters.HTTPAdapter
        """
        self._cache = DictionaryCache() if cache_backend is None else cache_backend
        super(Basecamp3TransportAdapter, self).__init__(*args, **kwargs)

    def send(self, request, *args, **kwargs):
        """
        Calls the HTTPAdapter.send method with cache headers. Blocks if the request would exceed the rate limit.

        See also:
        https://github.com/basecamp/bc3-api#using-http-caching

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :type request: requests.PreparedRequest
        """
        self._set_cache_headers(request)
        method = request.method
        url = request.url
        logger.debug("Consulting with Semaphore")
        with Basecamp3TransportAdapter.SEMAPHORE:  # blocks here until rate limit has cooled off
            logger.debug("OK we can request now.")
            response = super(Basecamp3TransportAdapter, self).send(request, *args, **kwargs)
        if response.status_code == 304:  # not modified; cache hit
            cached_response = self._cache.get_cached_response(method, url)
            logger.debug("Returning a cached response for %s, %s", method, url)
            return cached_response
        else:
            self._cache_this_response(response)
            return response

    def _cache_this_response(self, response):
        """
        Cache the given HTTP response in the cache backend.

        :param response: the HTTP response to cache
        :type response: requests.Response
        """
        self._cache.set_cached(response)

    def _set_cache_headers(self, request):
        """
        If this request has been made before, get the ETag and Last-Modified headers from the response to it,
        and set the If-None-Match and If-Modified-Since headers on this new request.

        :param request: the HTTP request object to apply cache headers to
        :type request: requests.PreparedRequest
        """
        etag, last_modified = self._cache.get_cached_headers(request.method, request.url)
        if etag:
            request.headers['If-None-Match'] = etag
        if last_modified:
            request.headers['If-Modified-Since'] = last_modified
