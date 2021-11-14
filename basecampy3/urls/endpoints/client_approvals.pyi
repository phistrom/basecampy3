# -*- coding: utf-8 -*-
from typing import AnyStr, List, Literal, Optional

from .base import EndpointURLs
from .. import URL
from .._types import ClientApprovalOrID, ClientSideDict, PersonDict, ProjectOrID


class ClientApprovalResponseDict(ClientSideDict):
    type: Literal["Client::Approval::Response"]
    approved: bool


class ClientApprovalDict(ClientSideDict):
    type: Literal["Client::Approval"]
    subject: AnyStr
    due_on: Optional[AnyStr]
    replies_count: int
    replies_url: AnyStr
    approval_status: AnyStr  # TODO Literal["approved", ...?]
    approver: PersonDict
    responses: List[ClientApprovalResponseDict]


class ClientApprovals(EndpointURLs):
    def list(self, project: ProjectOrID) -> URL[List[ClientApprovalDict]]: ...

    def get(self, project: ProjectOrID,
            client_approval: ClientApprovalOrID) -> URL[ClientApprovalDict]: ...
