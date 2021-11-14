# -*- coding: utf-8 -*-
from typing import List, Literal

from .base import EndpointURLs
from .. import URL
from .._types import ClientSideDict, HasIDOrID, ProjectOrID


class ClientReplyDict(ClientSideDict):
    type: Literal["Client::Reply"]


class ClientReplies(EndpointURLs):

    def list(self, project: ProjectOrID, record: HasIDOrID) -> \
            URL[List[ClientReplyDict]]: ...


    def get(self, project: ProjectOrID, record: HasIDOrID,
            client_reply: int) -> URL[ClientReplyDict]: ...
