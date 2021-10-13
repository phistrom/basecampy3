from typing import ClassVar, Iterable, NoReturn, Optional, Type, Union

from ._base import BasecampObject, BasecampEndpoint
from . import projects


class MessageCategory(BasecampObject):
    id: int
    name: str
    icon: str
    created_at: str
    updated_at: str

    def edit(self, project: Union[projects.Project, int], name: bool, icon: bool) -> NoReturn: ...

    def delete(self, project: Union[projects.Project, int]) -> NoReturn: ...


class MessageCategories(BasecampEndpoint):
    OBJECT_CLASS: ClassVar[Type[MessageCategory]]

    CREATE_URL: ClassVar[str]
    DELETE_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    LIST_URL: ClassVar[str]
    UPDATE_URL: ClassVar[str]

    def create(self, name: str, icon: str, project: Union[projects.Project, int]) -> MessageCategory: ...

    def delete(self, project: Union[projects.Project, int], category: Union[MessageCategory, int]) -> NoReturn: ...

    def get(self, project: Union[projects.Project, int], category: Union[MessageCategory, int]) -> MessageCategory: ...

    def list(self, project: Union[projects.Project, int]) -> Iterable[MessageCategory]: ...

    def update(self, project: Union[projects.Project, int], category: Union[MessageCategory, int],
               name: Optional[Union[bool, str]],
               icon: Optional[Union[bool, str]]) -> NoReturn: ...
