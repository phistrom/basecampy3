# -*- coding: utf-8 -*-
"""
Base class for Recording objects in the Basecamp 3 API.
"""

import abc
from json import JSONDecodeError
from typing import Any, AnyStr, ClassVar, Iterable, List, Literal, Optional, TypedDict

from .base import EndpointURLs
from .. import URL
from .._types import RecordingDict, EventAction, HasIDOrID, PersonDict, PersonOrID, ProjectOrID, StatusString

SortBy = Literal["created_at", "updated_at"]
SortDirection = Literal["asc", "desc"]


class EventDict(TypedDict):
    id: int
    recording_id: int
    action: EventAction
    details: dict
    created_at: AnyStr
    creator: PersonDict


class SubscriptionDict(TypedDict):
    subscribed: bool
    count: int
    url: AnyStr
    subscribers: List[PersonDict]


class RecordingEndpointURLs(EndpointURLs, metaclass=abc.ABCMeta):

    RECORD_TYPE: ClassVar[AnyStr] = None

    def list(self, project: Optional[ProjectOrID] = None,
             status: StatusString = "active", sort: SortBy = "created_at",
             direction: SortDirection = "desc", **kwargs: Any) -> \
            URL[List[RecordingDict]]: ...

    def trash(self, project: ProjectOrID, recording: HasIDOrID) -> URL[JSONDecodeError]: ...

    def archive(self, project: ProjectOrID, recording: HasIDOrID) -> URL[JSONDecodeError]: ...

    def unarchive(self, project: ProjectOrID, recording: HasIDOrID): ...

    def client_visibility(self, project: ProjectOrID, recording: HasIDOrID,
                          visible_to_clients: bool) -> URL[RecordingDict]: ...

    def events(self, project: ProjectOrID, recording: HasIDOrID) -> URL[List[EventDict]]: ...

    def list_subscriptions(self, project: ProjectOrID, recording: HasIDOrID) -> URL[SubscriptionDict]: ...

    def subscribe_myself(self, project: ProjectOrID, recording: HasIDOrID) -> URL[SubscriptionDict]: ...

    def unsubscribe_myself(self, project: ProjectOrID, recording: HasIDOrID) -> URL[JSONDecodeError]: ...

    def update_subscriptions(self, project: ProjectOrID, recording: HasIDOrID,
                             subscriptions: Optional[Iterable[PersonOrID]] = None,
                             unsubscriptions: Optional[Iterable[PersonOrID]] = None,
                             **kwargs: Any) -> URL[SubscriptionDict]: ...
