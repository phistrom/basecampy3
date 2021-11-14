# -*- coding: utf-8 -*-

from typing import Any, AnyStr, Optional, TypedDict

from .base import EndpointURLs
from .. import URL


class AttachmentDict(TypedDict):
    attachable_sgid: AnyStr


class Attachments(EndpointURLs):
    def create(self, filepath: AnyStr, name: Optional[AnyStr] = None,
               content_type: Optional[AnyStr] = None, **kwargs: Any) -> URL[AttachmentDict]: ...
