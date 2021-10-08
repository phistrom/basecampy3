# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class People(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/people.md
    """
    def list(self):
        """
        Get all people visible to current user.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#get-all-people

        :return: the URL to retrieve a list of all People in this account
        :rtype: basecampy3.urls.URL
        """
        return self._get("/people.json")

    def list_by_project(self, project):
        """
        Get all active people on the given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#get-people-on-a-project

        :param project: the ID of a Project
        :type project: int
        :return: the URL for getting a list of People on the desired Project
        :rtype: basecampy3.urls.URL
        """
        return self._get("/projects/{project}/people.json", project=project)

    def list_pingable(self):
        """
        Get People who can be pinged.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#get-pingable-people

        :return: the URL to get a list of people who can be pinged
        :rtype: basecampy3.urls.URL
        """

        return self._get("/circles/people.json")

    def get(self, person):
        """
        Get a Person by their ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#get-person

        :param person: the ID of a Person
        :type person: int
        :return: the URL to get the desired Person
        :rtype: basecampy3.urls.URL
        """
        return self._get("/people/{person}.json")

    def get_myself(self):
        """
        Get the currently logged in user's Person object.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#get-my-personal-info

        :return: the URL to access your own Person object
        :rtype: basecampy3.urls.URL
        """
        return self._get("/my/profile.json")
