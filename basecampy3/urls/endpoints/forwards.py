# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs


class Forwards(RecordingEndpointURLs):
    """
    Email Forwards.

    https://3.basecamp-help.com/article/58-forwards
    https://github.com/basecamp/bc3-api/blob/master/sections/forwards.md
    """

    RECORD_TYPE = "Inbox::Forward"

    # noinspection PyMethodOverriding
    def list(self, project, inbox):
        """
        Get a list of Forwards by Inbox.

        https://github.com/basecamp/bc3-api/blob/master/sections/forwards.md#get-forwards

        _The inherited list function for Recordings does not work for Inbox Forwards,
        hence the suppression of the inspection._

        :param project: the ID of a Project
        :type project: int
        :param inbox: the ID of an Inbox
        :type inbox: int
        :return: the URL to retrieve a list of Forwards for the desired Inbox
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/inboxes/{inbox}/forwards.json",
                         project=project, inbox=inbox)

    def get(self, project, forward):
        """
        Get a Forward by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/forwards.md#get-a-forward

        :param project: the ID of a Project
        :type project: int
        :param forward: the ID of a Forward
        :type forward: int
        :return: the URL to get the desired Forward
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/inbox_forwards/{forward}.json",
                         project=project, forward=forward)
