from typing import ClassVar, Iterable, Literal, NoReturn, Optional, Type, Union

from . import _types, projects, recordings, todolists


class TodoListGroup(todolists.TodoCollection):
    id: int
    status: _types.StatusString
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Todolist"]
    url: str
    app_url: str
    bookmark_url: str
    subscription_url: str
    comments_count: int
    comments_url: str
    position: int
    parent: _types.TodoListDict
    bucket: _types.ProjectDict
    creator: _types.CreatorDict
    description: str
    completed: bool
    completed_ratio: str
    name: str
    todos_url: str
    group_position_url: str
    app_todos_url: str

    def reposition(self, position: int) -> NoReturn: ...


class TodoListGroups(recordings.RecordingEndpoint):
    OBJECT_CLASS = ClassVar[Type[TodoListGroup]]

    LIST_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    CREATE_URL: ClassVar[str]
    REPOSITION_URL: ClassVar[str]

    def list(self, todolist: Union[todolists.TodoList, int],
             project: Union[projects.Project, int],
             status: _types.StatusString) -> Iterable[TodoListGroup]: ...

    def get(self, todolist_group: Union[TodoListGroup, int],
            project: Optional[Union[projects.Project, int]]) -> TodoListGroup: ...

    def create(self, name: str, todolist: Union[todolists.TodoList, int],
               project: Optional[Union[projects.Project, int]]) -> TodoListGroup: ...

    def reposition(self, position: int, todolist_group: Union[TodoListGroup, int],
                   project: Optional[Union[projects.Project, int]]) -> NoReturn: ...
