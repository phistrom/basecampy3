"""
Comments
https://github.com/basecamp/bc3-api/blob/master/sections/comments.md

Comments on all kinds of things.
"""

from dateutil import parser, tz
from . import _base
from .. import constants


class Comment(_base.RecordingBase):

    def __str__(self):
        try:
            created_at = parser.isoparse(self.created_at)
            created_at_local = created_at.astimezone(tz.tzlocal())
            created_at_formatted = created_at_local.strftime(constants.DATE_FORMAT)

            output = {
                "author": self.creator["name"],
                "email": self.creator["email_address"],
                "time": created_at_formatted,
                "content": self.content,
            }

            return "{author} <{email}> [{time}]: '{content}'".format(**output)
        except Exception:
            return super(Comment, self).__str__()


class Comments(_base.RecordingEndpointBase):
    OBJECT_CLASS = Comment

    LIST_URL = "{base_url}/buckets/{project_id}/recordings/{recording_id}/comments.json"
    GET_URL = "{base_url}/buckets/{project_id}/comments/{comment_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/recordings/{recording_id}/comments.json"
    UPDATE_URL = "{base_url}/buckets/{project_id}/comments/{comment_id}.json"

    def __init__(self, api, recording):
        super(Comments, self).__init__(api)
        self._recording = recording
        self._project_id = recording.project_id

    def list(self):
        """
        Get a list of comments for this Recording.

        :return: active comments on this Recording
        :rtype: collections.abc.Iterable[Comment]
        """
        recording_id = int(self._recording)
        url = self.LIST_URL.format(base_url=self.url, project_id=self._project_id, recording_id=recording_id)
        return self._get_list(url)

    def get(self, comment):
        """

        :param comment:
        :type comment: int|Comment
        :return:
        :rtype: Comment
        """
        comment_id = int(comment)
        url = self.GET_URL.format(base_url=self.url, project_id=self._project_id, comment_id=comment_id)
        return self._get(url)

    def create(self, content):
        """

        :param content:
        :type content: str
        :return:
        :rtype: Comment
        """
        recording_id = int(self._recording)
        data = {
            "content": content,
        }
        url = self.CREATE_URL.format(base_url=self.url, project_id=self._project_id, recording_id=recording_id)
        return self._create(url, data=data)

    def update(self, comment, content):
        """

        :param comment:
        :type comment: int|Comment
        :param content:
        :type content: str
        :return:
        :rtype: Comment
        """
        comment_id = int(comment)
        data = {
            "content": content
        }
        url = self.UPDATE_URL.format(base_url=self.url, project_id=self._project_id, comment_id=comment_id)
        return self._update(url, data=data)
