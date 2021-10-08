# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Inboxes(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/inboxes.md
    """
    def get(self, project, inbox):
        """
        Get an Inbox by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/inboxes.md#get-inbox

        :param project: the ID of a Project
        :type project: int
        :param inbox: the ID of an Inbox
        :type inbox: int
        :return: the URL to retrieve a specific Inbox's details
        :rtype: basecampy3.urls.URL
        """

        return self._get("/buckets/{project}/inboxes/{inbox}.json",
                         project=project, inbox=inbox)
