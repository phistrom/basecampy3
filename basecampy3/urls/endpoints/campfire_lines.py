# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class CampfireLines(EndpointURLs):
    def list(self, project, campfire, **kwargs):
        """
        Get a list of Campfire Lines.

        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#get-a-campfire

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param kwargs: additional query string parameters (not currently used)
        :type kwargs: str
        :return: a URL for retrieving lines of a Campfire
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/chats/{campfire}/lines.json",
                         project=project, campfire=campfire, params=kwargs)

    def get(self, project, campfire, line):
        """
        Get a Campfire Line by its project, campfire, and ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/campfires.md#get-a-campfire-line

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param line: the ID of a Campfire Line
        :type line: int
        :return: a Campfire Line
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/chats/{campfire}/lines/{line}.json",
                         project=project, campfire=campfire, line=line)

    def create(self, project, campfire):
        """
        Create a new Campfire Line (post a message to a Campfire).

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :return: a URL to post a new message to a Campfire
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/chats/{campfire}/lines.json",
                          project=project, campfire=campfire)

    def delete(self, project, campfire, line):
        """
        Delete a Campfire Line.

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param line: the ID of a Campfire Line
        :type line: int
        :return: the URL for deleting the specified Campfire Line
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/buckets/{project}/chats/{campfire}/lines/{line}.json",
                            project=project, campfire=campfire, line=line)
