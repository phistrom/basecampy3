from typing import ClassVar, Iterable, Literal, NoReturn, Optional, Type, Union

from ._base import BasecampEndpoint, BasecampObject
from . import _types, campfires


class CampfireLine(BasecampObject):
    id: int
    status: _types.StatusString
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Chat::Lines::Text"]
    url: str
    app_url: str
    bookmark_url: str
    parent: _types.CampfireDict
    bucket: _types.ProjectDict
    creator: _types.CreatorDict
    content: str


class CampfireLines(BasecampEndpoint):
    OBJECT_CLASS: ClassVar[Type[CampfireLine]]

    LIST_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    CREATE_URL: ClassVar[str]
    DELETE_URL: ClassVar[str]

    def list(self, project: Optional[_types.ProjectOrID],
             campfire: Optional[campfires.Campfire, int]) -> Iterable[CampfireLine]: ...

    def get(self, campfire_line: Union[CampfireLine, int],
            project: Optional[_types.ProjectOrID],
            campfire: Optional[campfires.Campfire, int]) -> CampfireLine: ...

    def create(self, content: str, project: Optional[_types.ProjectOrID],
               campfire: Optional[Union[campfires.Campfire, int]]) -> CampfireLine: ...

    def delete(self, campfire_line: Union[CampfireLine, int], project: Optional[_types.ProjectOrID],
               campfire: Optional[campfires.Campfire, int]) -> NoReturn: ...
