# -*- coding: utf-8 -*-
from typing import Any, AnyStr, ClassVar, List, Literal, Optional

from .recordings import RecordingEndpointURLs, SortBy, SortDirection
from .. import URL
from .._types import RecordingDict, CommentOrID, HasIDOrID, ProjectOrID, StatusString


class CommentDict(RecordingDict):
    type: Literal["Comment"]


class Comments(RecordingEndpointURLs):
    RECORD_TYPE: ClassVar[Literal["Comment"]]

    def client_visibility(self, project: ProjectOrID, recording: HasIDOrID,
                          visible_to_clients: bool) -> URL[CommentDict]: ...

    def list(self, project: Optional[ProjectOrID] = None,
             status: StatusString = "active", sort: SortBy = "created_at",
             direction: SortDirection = "desc", **kwargs: Any) -> \
            URL[List[CommentDict]]: ...

    def list_by_recording(self, project: ProjectOrID, recording: HasIDOrID) -> URL[List[CommentDict]]: ...

    def get(self, project: ProjectOrID, comment: CommentOrID) -> URL[CommentDict]: ...

    def create(self, project: ProjectOrID, recording: HasIDOrID, content: AnyStr, **kwargs: Any) -> URL[CommentDict]: ...

    def update(self, project: ProjectOrID, comment: CommentOrID, content: AnyStr, **kwargs: Any) -> URL[CommentDict]: ...
