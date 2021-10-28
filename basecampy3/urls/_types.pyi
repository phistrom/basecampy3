from typing import AnyStr, Iterable, Literal, Optional, TypedDict, Union

from basecampy3.endpoints.people import Person
from basecampy3.endpoints.projects import Project
from basecampy3.endpoints.templates import Template

PersonOrID = Union[int, Person]
"""A Person object or its ID as an integer."""

ProjectOrID = Union[int, Project]
"""A Project object or its ID as an integer."""

TemplateOrID = Union[int, Template]
"""A Template object or its ID as an integer."""

ProjectPeople = Iterable[PersonOrID]
"""A list of Person objects and/or their IDs for updating membership on a Project."""

HTTPVerb = Literal["GET", "POST", "PUT", "DELETE"]
"""All the HTTP verbs that the Basecamp 3 API uses."""

StatusString = Literal["archived", "trashed"]
"""Statuses accepted by the list() function of most endpoints."""

class CreatePersonDict(TypedDict):
    """
    Dictionaries used in :class:`basecampy3.urls.endpoints.Projects` for the
    ``create`` parameter of the ``update_membership`` function.
    """
    name: AnyStr
    email_address: AnyStr
    title: Optional[AnyStr]
    company_name: Optional[AnyStr]
