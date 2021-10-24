import json
import logging
import time
from datetime import datetime

from requests import adapters

from . import exc
from .cache import DictionaryCache
from .constants import RATE_LIMIT_PER_SECONDS, RATE_LIMIT_REQUESTS
from .rated_semaphore import RatedSemaphore

logger = logging.getLogger(__name__)


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

    def __init__(self, cache_backend=None, max_attempts=3, *args, **kwargs):
        """
        Applied to a ``requests.Session`` object to implement caching
        and rate-limiting.

        :param cache_backend: stores responses for later retrieval if the response is unchanged
        :type cache_backend: basecampy3.response_cache.ResponseCache
        :param max_attempts: number of times to retry a request if the response
                             is a retryable error (429, 5xx, etc.)
        :type max_attempts: int
        :param args: whatever args are supported by requests.adapters.HTTPAdapter
        :param kwargs: whatever kwargs are supported by requests.adapters.HTTPAdapter
        """
        self._cache = DictionaryCache() if cache_backend is None else cache_backend
        super(Basecamp3TransportAdapter, self).__init__(*args, **kwargs)
        self.max_attempts = max_attempts

    def send(self, request, *args, **kwargs):
        """
        Calls the HTTPAdapter.send method with cache headers. Blocks if the request would exceed the rate limit.

        See also:
        https://github.com/basecamp/bc3-api#using-http-caching

        :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
        :type request: requests.PreparedRequest
        """
        if request.method == "GET":
            self._set_cache_headers(request)

        # some errors are retry-able, but we only want to retry so many times...
        ex = None
        for attempt in range(0, self.max_attempts):
            logger.debug("Consulting with Semaphore")
            # blocks here until rate limit has cooled off
            with Basecamp3TransportAdapter.SEMAPHORE:
                logger.debug("OK we can request now.")
                try:
                    response = self._send(attempt, request, *args, **kwargs)
                    return response
                except exc.Basecamp3Error as ex:
                    logger.debug("On attempt %s/%s: %s", attempt+1, self.max_attempts, ex)
        else:
            raise ex

    def _cache_this_response(self, response):
        """
        Cache the given HTTP response in the cache backend.

        :param response: the HTTP response to cache
        :type response: requests.Response
        """
        self._cache.set_cached(response)

    @staticmethod
    def _handle_429(response):
        # default to one second delay if header missing
        retry_after = response.headers.get("Retry-After", 1.0)
        logger.debug("Received 429 error. Delaying for %s seconds.", retry_after)
        time.sleep(float(retry_after))

    @staticmethod
    def _log_rate_limit_header(response):
        try:
            rate_limit_json = response.headers["X-RateLimit"]
        except KeyError:
            return
        data = json.loads(rate_limit_json)
        until = datetime.strptime(data["until"], "%Y-%m-%dT%H:%M:%SZ")
        recharge_time = until - datetime.utcnow()
        seconds = round(recharge_time.seconds + (recharge_time.microseconds / 1000000), 2)
        logger.debug("X-RateLimit: %s/%s Remaining API Calls; "
                     "Time to Fully Recharge: %s seconds", data["remaining"],
                     data["limit"], seconds)

    def _send(self, attempt, request, *args, **kwargs):
        """
        Request send attempt. Called from the send() method's attempt loop so
        we can retry when we get a retryable error response.

        :param attempt: which attempt this is (1st, 2nd, ... etc)
        :type attempt: int
        :param request: the PreparedRequest to be sent
        :type request: requests.PreparedRequest
        :param args: additional parameters for the HTTPAdapter.send method
        :type args: typing.Any
        :param kwargs: additional parameters for the HTTPAdapter.send method
        :type kwargs: typing.Any
        :return: the Response to this request (or a previous Response if we
                 received a 304 response from the server)
        :rtype: requests.Response
        :raises Basecamp3Error: if we received anything other a 2xx or 304
                                HTTP response status code
        """
        response = super(Basecamp3TransportAdapter, self).send(request, *args, **kwargs)
        self._log_rate_limit_header(response)
        code = response.status_code

        print(request.method, request.url)
        print(response.headers.get("Cache-Control"))
        if code == 304:  # not modified; cache hit
            cached_response = self._cache.get_cached_response(request)
            logger.debug("Returning a cached response for %s, %s",
                         request.method, request.url)
            return cached_response
        elif code == 429:
            self._handle_429(response)  # delay
        elif 500 <= code < 600:  # 5xx error
            # delay for 2, 4, then 8 seconds
            delay_seconds = 2 ** (attempt + 1)
            time.sleep(delay_seconds)
        else:
            if response.ok and request.method == "GET":
                self._cache_this_response(response)
            return response

        raise exc.Basecamp3Error(response=response)

    def _set_cache_headers(self, request):
        """
        If this request has been made before, get the ETag and Last-Modified headers from the response to it,
        and set the If-None-Match and If-Modified-Since headers on this new request.

        :param request: the HTTP request object to apply cache headers to
        :type request: requests.PreparedRequest
        """
        etag, last_modified = self._cache.get_cached_headers(request)
        if etag:
            request.headers['If-None-Match'] = etag
        if last_modified:
            request.headers['If-Modified-Since'] = last_modified
