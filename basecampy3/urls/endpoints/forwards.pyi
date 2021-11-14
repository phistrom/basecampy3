# -*- coding: utf-8 -*-
from typing import Any, AnyStr, ClassVar, List, Literal, Optional, TypedDict

from .recordings import RecordingEndpointURLs, SortBy, SortDirection
from .. import URL
from .._types import BucketDict, ForwardOrID, InboxOrID, ParentDict, ProjectOrID, StatusString
from ...endpoints._types import CreatorDict

# because "from" is a keyword, we have to define our TypedDict like this
ForwardDict = TypedDict("ForwardDict", {
    "id": int,
    "status": AnyStr,
    "created_at": AnyStr,
    "updated_at": AnyStr,
    "title": AnyStr,
    "inherits_status": bool,
    "type": Literal["Inbox::Forward"],
    "url": AnyStr,
    "app_url": AnyStr,
    "parent": ParentDict,
    "bucket": BucketDict,
    "creator": CreatorDict,
    "content": AnyStr,
    "bookmark_url": AnyStr,
    "subscription_url": AnyStr,
    "subject": AnyStr,
    "from": AnyStr,
    "replies_count": int,
    "replies_url": AnyStr,
})


class Forwards(RecordingEndpointURLs):
    RECORD_TYPE: ClassVar[Literal["Inbox::Forward"]]

    def list(self, project: Optional[ProjectOrID] = None,
             status: StatusString = "active", sort: SortBy = "created_at",
             direction: SortDirection = "desc", **kwargs: Any) -> \
            URL[List[ForwardDict]]: ...

    def list_by_inbox(self, project: ProjectOrID, inbox: InboxOrID) -> \
            URL[List[ForwardDict]]: ...

    def get(self, project: ProjectOrID, forward: ForwardOrID) -> \
            URL[ForwardDict]: ...
