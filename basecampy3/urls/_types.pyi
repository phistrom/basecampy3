from typing import AnyStr, Generic, Iterable, Literal, Optional, Protocol, TypedDict, TypeVar, Union

from requests import Response

from basecampy3.endpoints.campfire_lines import CampfireLine
from basecampy3.endpoints.campfires import Campfire
from basecampy3.endpoints.chatbots import Chatbot
from basecampy3.endpoints.client_approvals import ClientApproval
from basecampy3.endpoints.comments import Comment
from basecampy3.endpoints.documents import Document
from basecampy3.endpoints.forwards import Forward
from basecampy3.endpoints.inbox_replies import InboxReply
from basecampy3.endpoints.inboxes import Inbox
from basecampy3.endpoints.people import Person
from basecampy3.endpoints.projects import Project
from basecampy3.endpoints.templates import Template
from basecampy3.endpoints.vaults import Vault

T = TypeVar("T")


class GenericJSONResponse(Response, Generic[T]):
    def json(self, **kwargs) -> T: ...


class HasID(Protocol):
    id: int


HasIDOrID = Union[int, HasID]
"""An object with a ``id`` field or its ID as an integer."""

CampfireOrID = Union[int, Campfire]
"""A Campfire object or its ID as an integer."""

CampfireLineOrID = Union[int, CampfireLine]
"""A Campfire Line object or its ID as an integer."""

ChatbotOrID = Union[int, Chatbot]
"""A Chatbot object or its ID as an integer."""

ClientApprovalOrID = Union[int, ClientApproval]
"""A ClientApproval object or its ID as an integer."""

CommentOrID = Union[int, Comment]
"""A Comment object or its ID as an integer."""

DocumentOrID = Union[int, Document]
"""A Document object or its ID as an integer."""

InboxOrID = Union[int, Inbox]
"""An Inbox object or its ID as an integer."""

InboxReplyOrID = Union[int, InboxReply]
"""An Inbox Reply object or its ID as an integer."""

ForwardOrID = Union[int, Forward]
"""An Inbox Forward object or its ID as an integer."""

PersonOrID = Union[int, Person]
"""A Person object or its ID as an integer."""

ProjectOrID = Union[int, Project]
"""A Project object or its ID as an integer."""

TemplateOrID = Union[int, Template]
"""A Template object or its ID as an integer."""

VaultOrID = Union[int, Vault]
"""A Vault object or its ID as an integer."""

ProjectPeople = Iterable[PersonOrID]
"""A list of Person objects and/or their IDs for updating membership on a Project."""

HTTPVerb = Literal["GET", "POST", "PUT", "DELETE"]
"""All the HTTP verbs that the Basecamp 3 API uses."""

BucketType = Literal["Project"]
"""What can appear in a bucket dictionary's ``type`` field."""

EventAction = Literal["archived", "assignment_changed", "category_changed",
                      "completed", "completion_subscribers_changed",
                      "content_changed", "created", "description_changed",
                      "hidden_from_clients", "name_changed", "rescheduled",
                      "shared_with_clients", "subject_changed",
                      "summary_changed", "title_changed", "unarchived",
                      "uncompleted"]
"""Strings that can appear in the ``action`` field of an Event dictionary."""

ParentString = Literal["Document", "Message::Board", "Question", "Schedule",
                       "Todolist", "Todoset", "Vault"]
"""Types that can appear in a parent dictionary's ``type``."""

PersonableType = Literal["User"]
"""What can appear in a person dictionary's ``personable_type`` field."""

StatusString = Literal["archived", "trashed"]
"""Statuses accepted by the list() function of most endpoints."""


class CreatePersonDict(TypedDict):
    """
    Dictionaries used in :class:`basecampy3.urls.endpoints.Projects` for the
    ``create`` parameter of the ``update_membership`` function.
    """
    name: AnyStr
    email_address: AnyStr
    title: Optional[AnyStr]
    company_name: Optional[AnyStr]


class BucketDict(TypedDict):
    id: int
    name: AnyStr
    type: BucketType


class CompanyDict(TypedDict):
    id: int
    name: AnyStr


class PersonDict(TypedDict):
    id: int
    attachable_sgid: AnyStr
    name: AnyStr
    email_address: AnyStr
    personable_type: PersonableType
    title: AnyStr
    bio: AnyStr
    created_at: AnyStr
    updated_at: AnyStr
    admin: bool
    owner: bool
    client: bool
    time_zone: AnyStr
    avatar_url: AnyStr
    company: CompanyDict


class ParentDict(TypedDict):
    id: int
    title: AnyStr
    type: ParentString
    url: AnyStr
    app_url: AnyStr


class BasecampObjectDict(TypedDict):
    id: int
    status: AnyStr
    created_at: AnyStr
    updated_at: AnyStr
    title: AnyStr
    inherits_status: bool
    # this is where ``type:`` would go but we override it in child classes
    url: AnyStr
    app_url: AnyStr
    bookmark_url: AnyStr
    bucket: BucketDict
    creator: PersonDict
    content: AnyStr


class VisibilityDict(BasecampObjectDict):
    visible_to_clients: bool


class ChildDict(BasecampObjectDict):
    parent: ParentDict


class ClientSideDict(ChildDict):
    pass


class RecordingDict(ChildDict, VisibilityDict):
    pass


class CommentableDict(RecordingDict):
    comments_count: int
    comments_url: AnyStr


class SubscribeableDict(BasecampObjectDict):
    subscription_url: AnyStr


class PositionableDict(BasecampObjectDict):
    position: int
