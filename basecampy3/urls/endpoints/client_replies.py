# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class ClientReplies(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/client_replies.md
    """

    def list(self, project, record):
        """
        List the Client Replies to a given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_replies.md#get-client-replies

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL to list Client Replies
        :rtype: basecampy3.urls.URL
        """

        return self._get("/buckets/{project}/client/recordings/{record}/replies.json",
                         project=project, record=record)

    def get(self, project, record, client_reply):
        """
        Get a Client Reply by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_replies.md#get-a-client-reply

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :param client_reply: the ID of a Client Reply
        :type client_reply: int
        :return: the URL to retrieve the desired Client Reply
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/client/recordings/{record}/replies/{client_reply}.json",
                         project=project, record=record, client_reply=client_reply)
