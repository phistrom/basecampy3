# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class MessageBoards(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/message_boards.md
    """

    def get(self, project, board):
        """
        Get a Message Board by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/message_boards.md#get-message-board

        :param project: the ID of a Project
        :type project: int
        :param board: the ID of a Message Board
        :type board: int
        :return: the URL for the desired Message Board
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/message_boards/{board}.json",
                         project=project, board=board)
