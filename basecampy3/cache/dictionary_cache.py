from collections import OrderedDict
from .response_cache import ResponseCache
from .. import exc


class DictionaryCache(ResponseCache):
    """
    A simple cache used by default. Not good for multi-threaded or multi-host instances where you might need to cache
    your requests in something like Redis.
    """
    def __init__(self, max_entries=20):
        """
        :type max_entries: int
        """
        super(DictionaryCache, self).__init__()
        self.__max_entries = 0
        self.max_entries = max_entries
        self._cache_dict = OrderedDict()

    @property
    def max_entries(self):
        return self.__max_entries

    @max_entries.setter
    def max_entries(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("max_entries cannot be 0 or less.")
        self.__max_entries = value

    def get_cached_headers(self, request):
        try:
            key = self._request_to_hash(request)
            etag, last_modified, _ = self._cache_dict[key]
            return etag, last_modified
        except (KeyError, exc.UnhashableError):
            return None, None

    def get_cached_response(self, request):
        key = self._request_to_hash(request)
        item = self._cache_dict[key]
        # our cached items are a tuple as etag, last_modified, and response
        response = item[2]
        return response

    def set_cached(self, response):
        try:
            key = self._request_to_hash(response.request)
        except exc.UnhashableError:
            return
        etag = response.headers.get('ETag')
        last_modified = response.headers.get('Last-Modified')
        self._add_to_cache(key, etag, last_modified, response)

    def _add_to_cache(self, key, etag, last_modified, response):
        """
        Handle adding a new entry to the cache, popping off cache entries in a FIFO order if the dictionary exceeds
        the maximum size.

        :param key: the unique key to use to store this item for lookup later, i.e. tuple(method, url)
        :type key: typing.Hashable
        :param etag: the ETag provided in the response for easy access later
        :type etag: str
        :param last_modified: the Last-Modified header in the response for easy access later
        :type last_modified: str
        :param response: the entire response object
        :type response: requests.Response
        """
        item = (etag, last_modified, response)

        # ensure it's the freshest item in the dict
        try:
            self._cache_dict.move_to_end(key)
        except KeyError:
            pass

        self._cache_dict[key] = item

        # pop off oldest entries until within limit
        while len(self._cache_dict) >= self.max_entries:
            self._cache_dict.popitem(last=False)
