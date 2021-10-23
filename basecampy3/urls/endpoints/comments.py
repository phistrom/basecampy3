# -*- coding: utf-8 -*-
"""
URLs related to Chatbot objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs


class Comments(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/comments.md
    """

    RECORD_TYPE = "Comment"

    def list_by_recording(self, project, recording):
        """
        Get a list of Comments on the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL to use to get a list of Comments from the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/recordings/{recording}/comments.json",
                         project=project, recording=recording)

    def get(self, project, comment):
        """
        Get a Comment by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-a-comment

        :param project: the ID of a Project
        :type project: int
        :param comment: the ID of a Comment
        :type comment: int
        :return: the URL to retrieve the desired Comment
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/comments/{comment}.json",
                         project=project, comment=comment)

    def create(self, project, recording, content, **kwargs):
        """
        Post a new Comment on the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#create-a-comment

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Record
        :type recording: int
        :param content: rich text (HTML) content of the Comment
        :type content: typing.AnyStr
        :param kwargs: additional parameters for JSON (not currently used)
        :type kwargs: typing.AnyStr
        :return: the URL to use for creating a new Comment on the desired Recording
        :rtype: basecampy3.urls.URL
        """
        kwargs["content"] = content
        return self._post("/buckets/{project}/recordings/{recording}/comments.json",
                          project=project, recording=recording, json_dict=kwargs)

    def update(self, project, comment, content, **kwargs):
        """
        Modify the content of the given Comment.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#update-a-comment

        :param project: the ID of a Project
        :type project: int
        :param comment: the ID of a Comment
        :type comment: int
        :param content: rich text (HTML) to change the Comment to
        :type content: typing.AnyStr
        :param kwargs: additional JSON parameters (not currently used)
        :type kwargs: typing.AnyStr
        :return: the URL to use to modify the desired Comment
        :rtype: basecampy3.urls.URL
        """
        kwargs["content"] = content

        return self._put("/buckets/{project}/comments/{comment}.json",
                         project=project, comment=comment, json_dict=kwargs)
