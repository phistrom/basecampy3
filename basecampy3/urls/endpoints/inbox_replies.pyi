# -*- coding: utf-8 -*-
from typing import List, Literal

from .base import EndpointURLs
from .. import URL
from .._types import ForwardOrID, InboxReplyOrID, ProjectOrID, RecordingDict


class InboxReplyDict(RecordingDict):
    type: Literal["Inbox::Reply"]


class InboxReplies(EndpointURLs):
    def list(self, project: ProjectOrID, forward: ForwardOrID) -> \
            URL[List[InboxReplyDict]]: ...

    def get(self, project: ProjectOrID, forward: ForwardOrID,
            reply: InboxReplyOrID) -> URL[InboxReplyDict]: ...
