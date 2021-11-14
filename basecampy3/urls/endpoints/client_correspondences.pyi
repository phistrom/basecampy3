# -*- coding: utf-8 -*-
from typing import AnyStr, List, Literal

from .base import EndpointURLs
from .. import URL
from .._types import ClientSideDict, ProjectOrID


class ClientCorrespondenceDict(ClientSideDict):
    type: Literal["Client::Correspondence"]
    subject: AnyStr
    replies_count: int
    replies_url: AnyStr


class ClientCorrespondences(EndpointURLs):
    def list(self, project: ProjectOrID) -> \
            URL[List[ClientCorrespondenceDict]]: ...

    def get(self, project: ProjectOrID, client_correspondence: int) -> \
            URL[ClientCorrespondenceDict]: ...
