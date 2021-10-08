# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class MessageTypes(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md
    """
    def list(self, project):
        """
        Get a list of Message Board Message Types (categories) for a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md#get-message-types

        :param project: the ID of a Project
        :type project: int
        :return: the URL to retrieve a list of Message Types for the desired Project
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/categories.json",
                         project=project)

    def get(self, project, message_type):
        """
        Get a Message Type by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md#get-a-message-type

        :param project: the ID of a Project
        :type project: int
        :param message_type: the ID of a Message Type
        :type message_type: int
        :return: the URL to get the desired Message Type
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/categories/{message_type}.json",
                         project=project, message_type=message_type)

    def create(self, project):
        """
        Create a new Message Type (category).

        https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md#create-a-message-type

        :param project: the ID of a Project
        :type project: int
        :return: the URL to create a new Message Type in the desired Project
        :rtype: basecampy3.urls.URL
        """

    def update(self, project, message_type):
        """
        Update a Message Type by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md#update-a-message-type

        :param project: the ID of a Project
        :type project: int
        :param message_type: the ID of a Message Type
        :type message_type: int
        :return: the URL for updating the desired Message Type
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/categories/{message_type}.json",
                         project=project, message_type=message_type)

    def delete(self, project, message_type):
        """
        Delete a Message Type by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/message_types.md#destroy-a-message-type

        :param project: the ID of a Project
        :type project: int
        :param message_type: the ID of a Message Type
        :type message_type: int
        :return: the URL to delete the desired Message Type
        :rtype: basecampy3.urls.URL
        """

        return self._delete("/buckets/{project}/categories/{message_type}.json",
                            project=project, message_type=message_type)
