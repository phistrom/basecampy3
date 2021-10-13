import datetime
from typing import Literal, Optional, TypedDict, Union

from . import projects


class CampfireDict(TypedDict):
    id: int
    title: str
    type: Literal["Chat::Transcript"]
    url: str
    app_url: str


class CompanyDict(TypedDict):
    id: int
    name: str


class CreatorDict(TypedDict):
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


DateString = Union[str, datetime.datetime, datetime.date]


class ProjectDict(TypedDict):
    id: int
    name: str
    type: Literal["Project"]


ProjectOrID = Union[projects.Project, int]

StatusString = Literal["active", "archived", "trashed"]


class TodoListDict(TypedDict):
    id: int
    title: str
    type: Literal["Todolist"]
    url: str
    app_url: str
