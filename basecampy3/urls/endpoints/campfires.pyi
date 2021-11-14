# -*- coding: utf-8 -*-
from typing import AnyStr, List, Literal

from .base import EndpointURLs
from .. import URL
from .._types import CampfireOrID, PositionableDict, ProjectOrID, SubscribeableDict, VisibilityDict


class CampfireDict(SubscribeableDict, PositionableDict, VisibilityDict):
    type: Literal["Chat::Transcript"]
    topic: Literal["Campfire"]
    lines_url: AnyStr


class Campfires(EndpointURLs):
    def list(self, **kwargs: AnyStr) -> URL[List[CampfireDict]]: ...

    def get(self, project: ProjectOrID, campfire: CampfireOrID) -> \
            URL[CampfireDict]: ...
