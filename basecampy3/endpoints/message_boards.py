from ._base import BasecampEndpoint, BasecampObject


class MessageBoard(BasecampObject):
    """
    A Message Board for posting Messages to.
    """

    def post_message(self, subject, content=None, status="active", category=None):
        """
        Creates a new Message on this MessageBoard.

        :param subject: the subject or title of this Message
        :type subject: str
        :param content: the HTML-formatted body of the message
        :type content: str
        :param status: set to "active" for the message to be live immediately
        :type status: str
        :param category: a MessageCategory object or ID
        :type category: basecampy3.endpoints.message_categories.MessageCategory|int
        :return: the newly created Message object
        :rtype: basecampy3.endpoints.messages.Message
        """
        return self._endpoint._api.messages.create(subject=subject, content=content, status=status,
                                                   category=category, board=self)

    def list(self):
        """
        :return: a list of Message threads on this board.
        :rtype: collections.Iterable[basecampy3.endpoints.messages.Message]
        """
        return self._endpoint._api.messages.list(board=self)

    @property
    def message_types(self):
        return self._endpoint._api.message_categories.list(self.bucket['id'])

    def __int__(self):
        return int(self.id)


class MessageBoards(BasecampEndpoint):
    OBJECT_CLASS = MessageBoard

    GET_URL = "{base_url}/buckets/{project_id}/message_boards/{board_id}.json"

    def get(self, project, board=None):
        """
        Get a single Message Board. If you provide a Project object, you can omit the `board_id` parameter.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param board: a MessageBoard object or ID
        :type board: MessageBoard|int
        :return: a MessageBoard object if found, raises an error if not found
        :rtype: MessageBoard
        """

        project_id = int(project)
        board = int(board) if board else project.message_board.id

        url = self.GET_URL.format(base_url=self.url, project_id=project_id, board_id=board)
        return self._get(url)
