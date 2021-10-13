# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Chatbots(EndpointURLs):
    def list(self, project, campfire):
        """
        Get Chatbots in the given Campfire.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#get-chatbots

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :return: a URL to retrieve a list of Chatbots
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/chats/{campfire}/integrations.json",
                         project=project, campfire=campfire)

    def get(self, project, campfire, chatbot):
        """
        Get a Chatbot by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#get-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot: the ID of a Chatbot
        :type chatbot: int
        :return: the URL to retrieve the desired Chatbot
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/chats/{campfire}/integrations/{chatbot}.json",
                         project=project, campfire=campfire, chatbot=chatbot)

    def create(self, project, campfire):
        """
        Create a new Chatbot in the given Campfire.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :return: the URL for creating new Chatbots in the desired Campfire
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/chats/{campfire}/integrations.json",
                          project=project, campfire=campfire)

    def update(self, project, campfire, chatbot):
        """
        Update a Chatbot by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#update-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot: the ID of a Chatbot
        :type chatbot: int
        :return: the URL for updating the desired Chatbot
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/chats/{campfire}/integrations/{chatbot}.json",
                         project=project, campfire=campfire, chatbot=chatbot)

    def delete(self, project, campfire, chatbot):
        """
        Delete a Chatbot by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#destroy-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot: the ID of a Chatbot
        :type chatbot: int
        :return: the URl for deleting the desired Chatbot
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/buckets/{project}/chats/{campfire}/integrations/{chatbot}.json",
                            project=project, campfire=campfire, chatbot=chatbot)

    def create_line(self, project, campfire, chatbot_key):
        """
        Post a new message on a Campfire as a Chatbot.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-line

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot_key: the key of the Chatbot to post as
        :type chatbot_key: str
        :return: the URL to post messages as the desired Chatbot
        :rtype: basecampy3.urls.URL
        """

        return self._post("/integrations/{chatbot_key}/buckets/{project}/chats/{campfire}/lines.json",
                          chatbot_key=chatbot_key, project=project, campfire=campfire)


