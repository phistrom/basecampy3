# -*- coding: utf-8 -*-
"""
URLs related to Message objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs
from .. import util


class Messages(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/messages.md
    """

    RECORD_TYPE = "Message"

    def list_by_message_board(self, project, message_board):
        """
        Get a list of Messages from the given Message Board.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#get-messages

        :param project: the ID of a Project
        :type project: int
        :param message_board: the ID of a Message Board
        :type message_board: int
        :return: the URL to list Messages from the desired Message Board
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/message_boards/{message_board}/messages.json",
                         project=project, message_board=message_board)

    def get(self, project, message):
        """
        Get a Message.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#get-a-message

        :param project: the ID of a Project
        :type project: int
        :param message: the ID of a Message
        :type message: int
        :return: the URL to get the desired Message
        :rtype: basecampy3.urls.URl
        """

        return self._get("/buckets/{project}/messages/{message}.json",
                         project=project, message=message)

    def create(self, project, message_board, subject, content=None,
               status="active", category_id=None, **kwargs):
        """
        Create (post) a new Message on the given Message Board.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#create-a-message

        :param project: the ID of a Project
        :type project: int
        :param message_board: the ID of a Message Board
        :type message_board: int
        :param subject: the subject of this Message
        :type subject: typing.AnyStr
        :param content: the rich text content of this Message
        :type content: typing.AnyStr|None
        :param status: can be either "drafted" or "active" to publish immediately
        :type status: typing.AnyStr
        :param category_id: the Message Type of the new Message
        :type category_id: int|basecampy3.endpoints.message_types.MessageType|None
        :return: the URL to use to create a new message on the desired Message Board
        :rtype: basecampy3.urls.URL
        """
        kwargs["subject"] = subject
        kwargs["content"] = content
        kwargs["status"] = status
        try:
            kwargs["category_id"] = category_id.id
        except AttributeError:
            kwargs["category_id"] = category_id

        kwargs = util.filter_unused(kwargs)
        return self._post("/buckets/{project}/message_boards/{message_board}/messages.json",
                          project=project, message_board=message_board, json_dict=kwargs)

    def update(self, project, message, subject=None, content=None, category_id=None, **kwargs):
        """
        Modify the subject, content, and/or category of the given Message.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#update-a-message

        :param project: the ID of a Project
        :type project: int
        :param message: the ID of a Message
        :type message: int
        :param subject: a new subject for this Message
        :type subject: typing.AnyStr|None
        :param content: replacement content for this Message
        :type content: typing.AnyStr|None
        :param category_id: the new Message Type for this Message
        :type category_id: int|basecampy3.endpoints.message_types.MessageType|None
        :param kwargs: additional JSON parameters (not currently used)
        :type kwargs: Any
        :return: the URL for updating the desired Message
        :rtype: basecampy3.urls.URL
        """
        kwargs["subject"] = subject
        kwargs["content"] = content

        try:
            kwargs["category_id"] = category_id.id
        except AttributeError:
            kwargs["category_id"] = category_id

        return self._put("/buckets/{project}/messages/{message}.json",
                         project=project, message=message, json_dict=kwargs)
