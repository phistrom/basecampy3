from . import _base, comments


class Recording(_base.RecordingBase):
    """
    Most of the data structures in the Basecamp 3 API are represented as "Recordings", with generic actions
    available to be performed.

    See also:
    https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md
    """
    def __init__(self, json_dict, endpoint):
        super(Recording, self).__init__(json_dict, endpoint)
        self._comments = None

    @property
    def comments(self):
        comment_count = self._values.get("comments_count")
        if comment_count is None:
            # ex = "'%s' object has no attribute 'comments'" % type(self).__name__
            raise AttributeError()
        if self._comments is None:
            self._comments = comments.Comments(self._endpoint._api, self)
        return self._comments


class RecordingEndpoint(_base.RecordingEndpointBase):
    OBJECT_CLASS = Recording
