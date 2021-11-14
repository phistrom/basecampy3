# -*- coding: utf-8 -*-
from json import JSONDecodeError
from typing import AnyStr, List, Optional, TypedDict

from .base import EndpointURLs
from .. import URL
from .._types import CampfireOrID, ChatbotOrID, ProjectOrID


class ChatbotDict(TypedDict):
    id: int
    created_at: AnyStr
    updated_at: AnyStr
    service_name: AnyStr
    command_url: Optional[AnyStr]
    url: AnyStr
    app_url: AnyStr
    lines_url: AnyStr


class Chatbots(EndpointURLs):
    def list(self, project: ProjectOrID, campfire: CampfireOrID) -> URL[List[ChatbotDict]]: ...

    def get(self, project: ProjectOrID, campfire: CampfireOrID, chatbot: ChatbotOrID) -> URL[ChatbotDict]: ...

    def create(self, project: ProjectOrID, campfire: CampfireOrID, service_name: AnyStr,
               command_url: AnyStr = None) -> URL[ChatbotDict]: ...

    def update(self, project: ProjectOrID, campfire: CampfireOrID, chatbot: ChatbotOrID,
               service_name: AnyStr = None, command_url: AnyStr = None) -> URL[ChatbotDict]: ...

    def delete(self, project: ProjectOrID, campfire: CampfireOrID, chatbot: ChatbotOrID) -> URL[JSONDecodeError]: ...

    def create_line(self, project: ProjectOrID, campfire: CampfireOrID, chatbot_key: AnyStr,
                    content: AnyStr) -> URL: ...
