from collections import OrderedDict
from .response_cache import ResponseCache


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
        if value < 0:
            raise ValueError("max_entries cannot be negative")
        self.__max_entries = value

    def get_cached_headers(self, method, url):
        try:
            key = (method, url)
            etag, last_modified, _ = self._cache_dict[key]
            return etag, last_modified
        except KeyError:
            return None, None

    def get_cached_response(self, method, url):
        item = self._cache_dict[(method, url)]
        response = item[2]  # our cached items are a tuple as etag, last_modified, and response
        return response

    def set_cached(self, response):
        key = (response.request.method, response.request.url)
        etag = response.headers.get('ETag')
        last_modified = response.headers.get('Last-Modified')
        self._add_to_cache(key, etag, last_modified, response)

    def _add_to_cache(self, key, etag, last_modified, response):
        """
        Handle adding a new entry to the cache, popping off cache entries in a FIFO order if the dictionary exceeds
        the maximum size.

        :param key: the unique key to use to store this item for lookup later, i.e. tuple(method, url)
        :type key: tuple[str]
        :param etag: the ETag provided in the response for easy access later
        :type etag: str
        :param last_modified: the Last-Modified header in the response for easy access later
        :type last_modified: str
        :param response: the entire response object
        :type response: requests.Response
        """
        item = (etag, last_modified, response)

        try:
            del self._cache_dict[key]  # pop this response out of the cache if it's in there already
        except KeyError:
            pass

        while len(self._cache_dict) >= self.max_entries:  # pop off oldest entries until within limit
            self._cache_dict.popitem(last=False)

        # it's now the freshest item in the cache
        self._cache_dict[key] = item
