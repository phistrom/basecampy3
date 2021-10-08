# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class InboxReplies(EndpointURLs):
    def list(self, project, forward):
        """
        Get Inbox Replies to the given Forward.

        https://github.com/basecamp/bc3-api/blob/master/sections/inbox_replies.md#get-inbox-replies

        :param project: the ID of a Project
        :type project: int
        :param forward: the ID of a Forward
        :type forward: int
        :return: the URL for retrieving a list of Inbox Replies
        :rtype: basecampy3.urls.URL
        """

        return self._get("/buckets/{project}/inbox_forwards/{forward}/replies.json",
                         project=project, forward=forward)

    def get(self, project, forward, reply):
        """
        Get an Inbox Reply by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/inbox_replies.md#get-an-inbox-reply

        :param project: the ID of a Project
        :type project: int
        :param forward: the ID of a Forward
        :type forward: int
        :param reply: the ID of an Inbox Reply
        :type reply: int
        :return: the URL to retrieve a desired Inbox Reply
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/inbox_forwards/{forward}/replies/{reply}.json",
                         project=project, forward=forward, reply=reply)
