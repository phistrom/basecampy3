# -*- coding: utf-8 -*-
"""
URLs related to Chatbot objects in the Basecamp 3 API.
"""

from .base import EndpointURLs
from .. import util


class Chatbots(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md
    """
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

    def create(self, project, campfire, service_name, command_url=None):
        """
        Create a new Chatbot in the given Campfire.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param service_name: the name of the chatbot
        :type service_name: typing.AnyStr
        :param command_url: the URL Basecamp can call when the bot is addressed
        :type command_url: typing.AnyStr|None
        :return: the URL for creating new Chatbots in the desired Campfire
        :rtype: basecampy3.urls.URL
        """
        json_dict = {
            "service_name": service_name,
            "command_url": command_url,
        }
        return self._post("/buckets/{project}/chats/{campfire}/integrations.json",
                          project=project, campfire=campfire, json_dict=json_dict)

    def update(self, project, campfire, chatbot, service_name=None, command_url=None):
        """
        Update a Chatbot by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#update-a-chatbot

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot: the ID of a Chatbot
        :type chatbot: int
        :param service_name: a new name for the chatbot
        :type service_name: typing.AnyStr
        :param command_url: a new URL for Basecamp to call when the bot is addressed
        :type command_url: typing.AnyStr|None
        :return: the URL for updating the desired Chatbot
        :rtype: basecampy3.urls.URL
        """
        json_dict = {
            "service_name": service_name,
            "command_url": command_url,
        }
        json_dict = util.filter_unused(json_dict)
        return self._put("/buckets/{project}/chats/{campfire}/integrations/{chatbot}.json",
                         project=project, campfire=campfire,
                         chatbot=chatbot, json_dict=json_dict)

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

    def create_line(self, project, campfire, chatbot_key, content):
        """
        Post a new message on a Campfire as a Chatbot.

        https://github.com/basecamp/bc3-api/blob/master/sections/chatbots.md#create-a-line

        :param project: the ID of a Project
        :type project: int
        :param campfire: the ID of a Campfire
        :type campfire: int
        :param chatbot_key: the key of the Chatbot to post as
        :type chatbot_key: str
        :param content: the content of the message in rich text (HTML)
        :type content: typing.AnyStr
        :return: the URL to post messages as the desired Chatbot
        :rtype: basecampy3.urls.URL
        """

        json_dict = {
            "content": content
        }

        return self._post("/integrations/{chatbot_key}/buckets/{project}/chats/{campfire}/lines.json",
                          chatbot_key=chatbot_key, project=project,
                          campfire=campfire, json_dict=json_dict)
