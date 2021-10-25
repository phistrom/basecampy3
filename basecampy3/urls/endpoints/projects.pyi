# -*- coding: utf-8 -*-
from typing import Any, AnyStr, Iterable, Optional

from .._types import CreatePersonDict, ProjectOrID, ProjectPeople, StatusString, TemplateOrID
from .base import EndpointURLs
from ..url import URL


class Projects(EndpointURLs):

    def list(self, status: StatusString = None, **kwargs: Any) -> URL: ...

    def get(self, project: ProjectOrID) -> URL: ...

    def create(self, name: AnyStr, description: Optional[AnyStr] = None,
               **kwargs: Any) -> URL: ...

    def update(self, project: ProjectOrID, name: Optional[AnyStr] = None,
               description: Optional[AnyStr] = None, **kwargs: Any) -> URL: ...

    def trash(self, project: ProjectOrID) -> URL: ...

    def update_membership(self, project: ProjectOrID,
                          grant: Optional[ProjectPeople] = None,
                          revoke: Optional[ProjectPeople] = None,
                          create: Iterable[CreatePersonDict] = None,
                          **kwargs: Any) -> URL: ...

    def create_from_template(self, template: TemplateOrID,
                             name: AnyStr,
                             description: Optional[AnyStr] = None,
                             **kwargs: Any) -> URL: ...

    def get_construction_status(self, template: TemplateOrID, project_construction: int) -> URL: ...
