import logging
from requests import adapters
from .rated_semaphore import RatedSemaphore
from .dictionary_cache import DictionaryCache
from .constants import RATE_LIMIT_PER_SECONDS, RATE_LIMIT_REQUESTS


class Basecamp3TransportAdapter(adapters.HTTPAdapter):
    """
    Handles API request caching and rate limiting.
    """

    # See https://github.com/basecamp/bc3-api#rate-limiting-429-too-many-requests
    # keeps us under the limit
    SEMAPHORE = RatedSemaphore(RATE_LIMIT_REQUESTS, RATE_LIMIT_PER_SECONDS)

    def __init__(self, cache_backend=None, *args, **kwargs):
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
        logging.debug("Consulting with Semaphore")
        with Basecamp3TransportAdapter.SEMAPHORE:  # blocks here until rate limit has cooled off
            logging.debug("OK we can request now.")
            response = super(Basecamp3TransportAdapter, self).send(request, *args, **kwargs)
        if response.status_code == 304:  # not modified; cache hit
            cached_response = self._cache.get_cached_response(method, url)
            return cached_response
        else:
            self._cache_this_response(response)
            return response

    def _cache_this_response(self, response):
        url = response.request.url
        self._cache.set_cached(response)

    def _set_cache_headers(self, request):
        """
        If this request has been made before, get the ETag and Last-Modified headers from the response to it,
        and set the If-None-Match and If-Modified-Since headers on this new request.


        :type request: requests.PreparedRequest
        """
        etag, last_modified = self._cache.get_cached_headers(request.method, request.url)
        if etag:
            request.headers['If-None-Match'] = etag
        if last_modified:
            request.headers['If-Modified-Since'] = last_modified
