# -*- coding: utf-8 -*-
from typing import Any, AnyStr, ClassVar, List, Literal, Optional

from .recordings import RecordingEndpointURLs, SortBy, SortDirection
from .. import URL
from .._types import RecordingDict, CommentableDict, DocumentOrID, HasIDOrID, ProjectOrID, StatusString, VaultOrID


class DocumentDict(RecordingDict, CommentableDict):
    type: Literal["Document"]
    subscription_url: AnyStr
    position: int


DocumentStatus = Literal["drafted", "published"]


class Documents(RecordingEndpointURLs):
    RECORD_TYPE: ClassVar[Literal["Document"]]

    def client_visibility(self, project: ProjectOrID, recording: HasIDOrID,
                          visible_to_clients: bool) -> URL[DocumentDict]: ...

    def list(self, project: Optional[ProjectOrID] = None,
             status: StatusString = "active", sort: SortBy = "created_at",
             direction: SortDirection = "desc", **kwargs: Any) -> \
            URL[List[DocumentDict]]: ...

    def list_by_vault(self, project: ProjectOrID, vault: VaultOrID) -> \
            URL[List[DocumentDict]]: ...

    def get(self, project: ProjectOrID, document: DocumentOrID) -> \
            URL[DocumentDict]: ...

    def create(self, project: ProjectOrID, vault: VaultOrID, title: AnyStr,
               content: AnyStr, status: Optional[DocumentStatus] = None) -> \
            URL[DocumentDict]: ...

    def update(self, project: ProjectOrID, document: DocumentOrID,
               title: Optional[AnyStr] = None,
               content: Optional[AnyStr] = None) -> URL[DocumentDict]: ...
