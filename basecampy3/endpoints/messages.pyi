from typing import ClassVar, Iterable, Literal, NoReturn, Optional, Type, TypedDict, Union

from . import _types, message_categories, message_boards, projects, recordings


class MessageBoardDict(TypedDict):
    id: int
    title: str
    type: Literal["Message::Board"]
    url: str
    app_url: str


class Message(recordings.Recording):
    id: int
    status: str
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Message"]
    url: str
    app_url: str
    bookmark_url: str
    subscription_url: str
    comments_count: int
    comments_url: str
    parent: MessageBoardDict
    bucket: _types.ProjectDict
    creator: _types.CreatorDict
    content: str
    subject: str

    def edit(self, subject: Optional[Union[bool, str]], content: Optional[Union[bool, str]],
             category: Optional[Union[message_categories.MessageCategory,bool,int]]) -> NoReturn: ...

    @property
    def icon(self) -> str: ...

    @property
    def message_board(self) -> message_boards.MessageBoard: ...


class Messages(recordings.RecordingEndpoint):
    OBJECT_CLASS = ClassVar[Type[Message]]

    CREATE_URL: ClassVar[str]
    GET_URL: ClassVar[str]
    LIST_URL: ClassVar[str]
    UPDATE_URL: ClassVar[str]

    def create(self, subject: str, content: Optional[str], status: Optional[_types.StatusString],
               category: Optional[Union[message_categories.MessageCategory,int]],
               project: Optional[projects.Project,int],
               board: Optional[Union[projects.Project,int]]) -> Message: ...

    def get(self, message: Union[Message, int], project: Optional[projects.Project, int]) -> Message: ...

    def list(self, project: Optional[Union[projects.Project,int]],
             board: Optional[message_boards.MessageBoard,int]) -> Iterable[Message]: ...

    def update(self, subject: Optional[Union[bool, str]], content: Optional[Union[bool, str]],
               category: Union[bool, message_categories.MessageCategory, int],
               project: Optional[Union[projects.Project,int]],
               message: Union[Message, int]) -> NoReturn: ...
