import datetime
from typing import ClassVar, Iterable, NoReturn, Optional, Type, Union

import re
import requests

from . import _base, answers, campfires, message_boards, people, templates, todosets
from ..exc import *


class Project(_base.BasecampObject):
    app_url: str
    bookmark_url: str
    bookmarked: str
    clients_enabled: bool
    created_at: datetime.datetime
    description: str
    dock: list[dict]
    id: int
    name: str
    purpose: str
    status: str
    updated_at: datetime
    url: str

    def add_new_user(self, name: str, email_address: str, title: Optional[str, None],
                     company_name: Optional[str, None]) -> people.Person: ...

    def modify_access(self, grant: Optional[Iterable[Union[people.Person, int]]],
                      revoke: Optional[Iterable[Union[people.Person, int]]]) -> requests.Response: ...

    def trash(self) -> NoReturn: ...

    def update(self, name: Optional[str], description: Optional[str]) -> NoReturn: ...

    @property
    def campfire(self) -> Optional[campfires.Campfire]: ...

    @property
    def message_board(self) -> Optional[message_boards.MessageBoard]: ...

    @property
    def todoset(self) -> Optional[todosets.TodoSet]: ...

    @property
    def people(self) -> Iterable[people.Person]: ...

    def list_answers_in_question(self, question: int) -> Iterable[answers.Answer]: ...

    def _get_dock_section(self, name: str) -> Optional[dict]: ...


class Projects(_base.BasecampEndpoint):
    OBJECT_CLASS: ClassVar[Type[Project]]

    CREATE_URL: str
    GET_URL: str
    LIST_URL: str
    MODIFY_ACCESS_URL: str
    TRASH_URL: str
    UPDATE_URL: str

    CREATION_FROM_TEMPLATE_TIMEOUT: int

    def add_new_user(self, project: Union[Project, int], name: str,
                     email_address: str, title: Optional[str],
                     company_name: Optional[str]) -> people.Person: ...

    def create(self, name: str, description: Optional[str],
               template: Optional[Union[templates.Template, int]]) -> Project: ...

    def find(self, any_: Optional[Union[re.Pattern, str]], name: Optional[Union[re.Pattern, str]],
             description: Optional[Union[re.Pattern, str]], status: Optional[Union[re.Pattern, str]],
             **kwargs) -> Iterable[Project]: ...

    @staticmethod
    def _is_project_a_match(project: Project, name_str: str, name_regex: re.Pattern,
                            desc_str: str, desc_regex: re.Pattern, any_: bool, **kwargs) -> bool: ...

    def get(self, project: Union[Project, int]) -> Project: ...

    def list(self, status: Optional[str]) -> Iterable[Project]: ...

    def modify_access(self, project: Union[Project, int], grant: Optional[Iterable[people.Person, int]],
                      revoke: Optional[Iterable[people.Person, int]]) -> requests.Response: ...

    def trash(self, project: Union[Project, int]) -> NoReturn: ...

    def update(self, project: Union[Project, int], name: Optional[str], description: Optional[str]) -> Project: ...

    def _create_from_template(self, name: str, description: str,
                              template: Union[templates.Template, int],
                              timeout: int) -> Project: ...
