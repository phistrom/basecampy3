from typing import ClassVar, Iterable, Literal, Optional, Type, Union

from ._base import BasecampObject, BasecampEndpoint
from . import _types, campfire_lines, projects


class Campfire(BasecampObject):
    id: int
    status: _types.StatusString
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Chat::Transcript"]
    url: str
    app_url: str
    bookmark_url: str
    subscription_url: str
    position: int
    bucket: _types.ProjectDict
    creator: _types.CreatorDict
    topic: str
    lines_url: str

    @property
    def lines(self) -> Iterable[campfire_lines.CampfireLine]: ...

    @property
    def project(self) -> Optional[projects.Project]: ...

    def post_message(self, content: str) -> campfire_lines.CampfireLine: ...


class Campfires(BasecampEndpoint):
    OBJECT_CLASS: ClassVar[Type[Campfire]]

    GET_URL: ClassVar[str]
    LIST_URL: ClassVar[str]

    def get(self, project: Optional[_types.ProjectOrID], campfire: Optional[Union[Campfire, int]]) -> Campfire: ...

    def list(self) -> Iterable[Campfire]: ...
