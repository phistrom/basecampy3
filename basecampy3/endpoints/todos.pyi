import datetime
from typing import ClassVar, Iterable, Literal, NoReturn, Optional, Type, Union

from . import _types, people, recordings, todolists, util
import six


class TodoItem(recordings.Recording):
    id: int
    status: _types.StatusString
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Todo"]
    url: str
    app_url: str
    bookmark_url: str
    subscription_url: str
    comments_count: int
    comments_url: str
    parent: _types.TodoListDict
    bucket: _types.ProjectDict
    creator: _types.CreatorDict
    description: str
    completed: bool
    content: str
    starts_on: Optional[str]
    due_on: Optional[str]
    assignees: Iterable
    completion_subscribers: Iterable
    completion_url: str

    def check(self) -> NoReturn: ...

    def uncheck(self) -> NoReturn: ...

    def reposition(self, position: int) -> NoReturn: ...

    def save(self, notify: bool) -> NoReturn: ...


class Todos(recordings.RecordingEndpoint):
    OBJECT_CLASS: ClassVar[Type[TodoItem]]
    LIST_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    CREATE_URL: ClassVar[str]
    UPDATE_URL: ClassVar[str]

    COMPLETE_URL: ClassVar[str]
    UNCOMPLETE_URL: ClassVar[str]
    REPOSITION_URL: ClassVar[str]

    def list(self, todolist: Union[todolists.TodoList],
             project: Optional[_types.ProjectOrID],
             status: Optional[_types.StatusString],
             completed: bool) -> Iterable[TodoItem]: ...

    def get(self, todoitem: Union[TodoItem, int], project: Optional[_types.ProjectOrID]) -> TodoItem: ...

    def create(self, content: str, todolist: Union[todolists.TodoList, int], project: Optional[_types.ProjectOrID],
               description: Optional[str], assignee_ids: Optional[Iterable[people.Person, int]],
               completion_subscriber_ids: Optional[Iterable[people.Person, int]], notify: bool,
               due_on: Optional[_types.DateString], starts_on: Optional[_types.DateString]) -> TodoItem: ...

    def update(self, todoitem: Union[TodoItem, int], project: Optional[_types.ProjectOrID],
               content: Optional[Union[str, bool]], description: Optional[Union[str, bool]],
               assignee_ids: Union[bool, Iterable[Union[people.Person, int]]],
               completion_subscriber_ids: Union[bool, Iterable[Union[people.Person, int]]],
               notify: bool, due_on: Optional[Union[bool, _types.DateString]],
               starts_on: Optional[Union[bool, _types.DateString]]) -> TodoItem: ...

    def complete(self, todoitem: Union[TodoItem, int], project: Optional[_types.ProjectOrID]) -> NoReturn: ...

    def uncomplete(self, todoitem: Union[TodoItem, int], project: Optional[_types.ProjectOrID]) -> NoReturn: ...

    def reposition(self, position: int, todoitem: Union[TodoItem, int],
                   project: Optional[_types.ProjectOrID]) -> NoReturn: ...

    @staticmethod
    def _normalize_date(somedate: _types.DateString) -> str: ...
