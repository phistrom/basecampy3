# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs


class Comments(RecordingEndpointURLs):
    RECORD_TYPE = "Comment"

    def list_by_recording(self, project, record):
        """
        Get a list of Comments on the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#get-comments

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL to use to get a list of Comments from the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/recordings/{record}/comments.json",
                         project=project, record=record)

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

    def create(self, project, record):
        """
        Post a new Comment on the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#create-a-comment

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Record
        :type record: int
        :return: the URL to use for creating a new Comment on the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/recordings/{record}/comments.json",
                          project=project, record=record)

    def update(self, project, comment):
        """
        Modify the content of the given Comment.

        https://github.com/basecamp/bc3-api/blob/master/sections/comments.md#update-a-comment

        :param project: the ID of a Project
        :type project: int
        :param comment: the ID of a Comment
        :type comment: int
        :return: the URL to use to modify the desired Comment
        :rtype: basecampy3.urls.URL
        """

        return self._put("/buckets/{project}/comments/{comment}.json",
                         project=project, comment=comment)


