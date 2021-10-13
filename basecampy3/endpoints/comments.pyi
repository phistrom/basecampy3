from typing import ClassVar, Iterable, Literal, Optional, TypedDict, Union

from . import _base, recordings
from ..bc3_api import Basecamp3


class TodoListDict(TypedDict):
    id: int
    title: str
    type: Literal["Todolist"]
    url: str
    app_url: str


class CompanyDict(TypedDict):
    id: int
    name: str


class PersonDict(TypedDict):
    id: int
    attachable_sgid: str
    name: str
    email_address: str
    personable_type: str
    title: str
    bio: Optional[str]
    created_at: str
    updated_at: str
    admin: bool
    owner: bool
    client: bool
    time_zone: str
    avatar_url: str
    company: CompanyDict



class ProjectDict(TypedDict):
    id: int
    name: str
    type: Literal["Project"]


class Comment(_base.RecordingBase):
    id: int
    status: Literal["active", "archived", "trashed"]
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Comment"]
    url: str
    app_url: str
    bookmark_url: str
    parent: TodoListDict
    bucket: ProjectDict
    content: str


class Comments(_base.RecordingEndpointBase):
    OBJECT_CLASS = Comment

    LIST_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    CREATE_URL: ClassVar[str]
    UPDATE_URL: ClassVar[str]

    def __init__(self, api: Basecamp3, recording: Union[recordings.Recording, int]): ...

    def list(self) -> Iterable[Comment]: ...

    def get(self, comment: Union[Comment, int]) -> Comment: ...

    def create(self, content: str) -> Comment: ...

    def update(self, comment: Union[Comment, int], content: str) -> Comment: ...
