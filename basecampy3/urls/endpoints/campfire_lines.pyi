# -*- coding: utf-8 -*-
from json import JSONDecodeError
from typing import Any, AnyStr, List, Literal

from .base import EndpointURLs
from .. import URL
from .._types import CampfireLineOrID, CampfireOrID, RecordingDict, ProjectOrID


class CampfireLineDict(RecordingDict):
    type: Literal["Chat::Lines::Text"]


class CampfireLines(EndpointURLs):

    def list(self, project: ProjectOrID, campfire: CampfireOrID,
             **kwargs: Any) -> URL[List[CampfireLineDict]]: ...

    def get(self, project: ProjectOrID, campfire: CampfireOrID,
            line: CampfireLineOrID) -> URL[CampfireLineDict]: ...

    def create(self, project: ProjectOrID, campfire: CampfireOrID,
               content: AnyStr) -> URL[CampfireLineDict]: ...

    def delete(self, project: ProjectOrID, campfire: CampfireOrID,
               line: CampfireLineOrID) -> URL[JSONDecodeError]: ...
