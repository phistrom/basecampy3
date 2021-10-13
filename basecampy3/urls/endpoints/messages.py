# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs


class Messages(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/messages.md
    """
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

    def create(self, project, message_board):
        """
        Create (post) a new Message on the given Message Board.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#create-a-message

        :param project: the ID of a Project
        :type project: int
        :param message_board: the ID of a Message Board
        :type message_board: int
        :return: the URL to use to create a new message on the desired Message Board
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/message_boards/{message_board}/messages.json",
                          project=project, message_board=message_board)

    def update(self, project, message):
        """
        Modify the subject, content, and/or category of the given Message.

        https://github.com/basecamp/bc3-api/blob/master/sections/messages.md#update-a-message

        :param project: the ID of a Project
        :type project: int
        :param message: the ID of a Message
        :type message: int
        :return: the URL for updating the desired Message
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/messages/{message}.json",
                         project=project, message=message)
