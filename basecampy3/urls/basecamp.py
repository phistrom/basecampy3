# -*- coding: utf-8 -*-
"""
"""

from . import endpoints
from .. import constants
from six.moves.urllib_parse import urljoin


class BasecampURLs(object):
    """
    Collection of URLs for accessing Basecamp resources.
    """

    def __init__(self, account_id, api_url=constants.API_URL):
        account_id = ("%s" % account_id).strip()  # convert from int to string for urljoin's sake
        base_url = urljoin(api_url, account_id)
        self._base_url = base_url
        self.attachments = endpoints.Attachments(base_url)
        self.campfire_lines = endpoints.CampfireLines(base_url)
        self.campfires = endpoints.Campfires(base_url)
        self.chatbots = endpoints.Chatbots(base_url)
        self.client_approvals = endpoints.ClientApprovals(base_url)
        self.client_correspondences = endpoints.ClientCorrespondences(base_url)
        self.client_replies = endpoints.ClientReplies(base_url)
        self.comments = endpoints.Comments(base_url)
        self.documents = endpoints.Documents(base_url)
        self.forwards = endpoints.Forwards(base_url)
        self.inbox_replies = endpoints.InboxReplies(base_url)
        self.inboxes = endpoints.Inboxes(base_url)
        self.message_boards = endpoints.MessageBoards(base_url)
        self.message_types = endpoints.MessageTypes(base_url)
        self.messages = endpoints.Messages(base_url)
        self.people = endpoints.People(base_url)
        self.projects = endpoints.Projects(base_url)
        self.questionnaires = endpoints.Questionnaires(base_url)
        self.todos = endpoints.Todos(base_url)
