from ..constants import DOCK_NAME_MESSAGE_BOARD
from . import recordings, util


class Message(recordings.Recording):
    """
    A Message that was posted on a Message Board. Not to be confused with a Campfire Line.
    """

    def edit(self, subject=False, content=False, category=False):
        """
        Change the subject, content, and/or category of this message.
        False is a placeholder for no-change. None erases the value like a blank string.

        :param subject: change the subject (title) of the message.
        :param content: change the body of the message
        :param category: change the category of the message
        """

        self._endpoint.update(subject=subject, content=content, category=category, message=self)

    @property
    def icon(self):
        try:
            return self.category['icon']
        except AttributeError:
            return ""

    @property
    def message_board(self):

        board_id = self.parent['id']
        project_id = self.bucket['id']
        return self._endpoint._api.message_boards.get(project=project_id, board=board_id)

    def __int__(self):
        return int(self.id)

    def __str__(self):
        try:
            text = "Message {id} Created by {creator} <{email}>: {icon} '{subject}'".format(
                id=self.id, creator=self.creator['name'], email=self.creator['email_address'], icon=self.icon,
                subject=self.subject
            )
            return text
        except:
            return super(Message, self).__str__()


class Messages(recordings.RecordingEndpoint):
    OBJECT_CLASS = Message

    CREATE_URL = "{base_url}/buckets/{project_id}/message_boards/{board_id}/messages.json"
    GET_URL = "{base_url}/buckets/{project_id}/messages/{message_id}.json"
    LIST_URL = "{base_url}/buckets/{project_id}/message_boards/{board_id}/messages.json"
    UPDATE_URL = "{base_url}/buckets/{project_id}/messages/{message_id}.json"

    def create(self, subject, content=None, status="active", category=None, project=None, board=None):
        """
        Create a new Message object. Either a project ID and MessageBoard ID must be given or just a MessageBoard
        object.

        :param subject: the subject (title) of this message
        :type subject: str
        :param content: the content (body) of this message. Can be HTML.
        :type content: str
        :param status: the status of this message. Set to "active" to post instantly. Required.
        :type status: str
        :param category: what category this message should be. MessageCategory objects vary by project.
        :type category: basecampy3.endpoints.message_categories.MessageCategory|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param board: the MessageBoard to post this message to. Either specify the object or the ID.
        :type board: basecampy3.endpoints.message_boards.MessageBoard|int
        :return: the newly posted Message
        :rtype: Message
        """
        project_id, board_id = util.project_or_object(project, board, section_name=DOCK_NAME_MESSAGE_BOARD)
        data = {
            "subject": subject,
            "status": status,
        }
        if content is not None:
            data["content"] = content
        if category is not None:
            data["category_id"] = int(category)
        url = self.CREATE_URL.format(base_url=self.url, project_id=project_id, board_id=board_id)
        message = self._create(url, data=data)
        return message

    def get(self, message, project=None):
        """
        Get a Message by using a Message object or a message ID with project ID.

        :param message: a Message object or ID
        :type message: Message|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :return: a Message object if found, raises an error if not found
        :rtype: Message
        """
        project_id, message_id = util.project_or_object(project, message)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, message_id=message_id)
        return self._get(url)

    def list(self, project=None, board=None):
        """
        Get a list of Messages from a given MessageBoard.

        :return: a list of Message objects
        :rtype: collections.Iterable[Message]
        """
        project_id, board_id = util.project_or_object(project, board, section_name=DOCK_NAME_MESSAGE_BOARD)
        url = self.LIST_URL.format(base_url=self.url, project_id=project_id, board_id=board_id)
        return self._get_list(url)

    def update(self, subject=False, content=False, category=False, project=None, message=None):
        """
        Change the subject, content, and/or category of a given message.
        False is a placeholder for no-change. None erases the value like a blank string.

        :param subject: change the subject (title) of the message.
        :type subject: str
        :param content: change the body of the message
        :type content: str
        :param category: change the category of the message
        :type category: basecampy3.endpoints.message_categories.MessageCategory|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param message: a Message object or ID
        :type message: Message|int
        """
        if subject is False and content is False and category is False:
            raise ValueError("At least one of subject, content, and category parameters should have a value to "
                             "be changed.")
        project_id, message_id = util.project_or_object(project, message, section_name=DOCK_NAME_MESSAGE_BOARD)
        data = {}
        if subject is not False:
            data['subject'] = "" if subject is None else subject
        if content is not False:
            data['content'] = "" if content is None else content
        if category is not False:
            data['category_id'] = int(category)
        url = self.UPDATE_URL.format(base_url=self.url, project_id=project_id, message_id=message_id)
        self._update(url, data=data)
