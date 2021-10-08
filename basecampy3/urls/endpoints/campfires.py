# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Campfires(EndpointURLs):
    def list(self, **kwargs):
        """
        Retrieve a list of Campfires.

        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#get-campfires

        :param kwargs: query string parameters (not currently used)
        :type kwargs: str
        :return: a URL for getting a list of Campfires
        :rtype: basecampy3.urls.URL
        """
        return self._get("/chats.json", params=kwargs)

    def get(self, project, campfire):
        """
        Retrieve a specific campfire by its project's ID and its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#get-a-campfire

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :return: a URL for getting a Campfire
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/chats/{campfire}.json", project=project, campfire=campfire)
