# -*- coding: utf-8 -*-
from typing import Any, AnyStr, Generic, Optional, TypeVar

from requests import Session
from six.moves.urllib_parse import urlencode

from ._types import GenericJSONResponse, HTTPVerb

T = TypeVar("T")

class URL(Generic[T]):
    url: AnyStr
    method: HTTPVerb
    filepath: Optional[AnyStr]
    _headers: dict
    _params: dict

    def __init__(self, url: AnyStr, method: HTTPVerb = "GET",
                 params: Optional[dict] = None,
                 headers: Optional[dict] = None,
                 filepath: Optional[AnyStr] = None,
                 json_dict: Optional[dict] = None): ...

    @property
    def params(self) -> dict: ...

    @params.setter
    def params(self, value: Optional[dict]): ...

    @property
    def headers(self) -> dict: ...

    @headers.setter
    def headers(self, value: Optional[dict]): ...

    def request(self, session: Optional[Session] = None, **kwargs: Any) -> GenericJSONResponse[T]: ...

    def __eq__(self, other: Any) -> bool:

    def __hash__(self) -> AnyStr: ...

    def __lt__(self, other: Any) -> bool: ...

    def __repr__(self) -> AnyStr: ...

    def __str__(self) -> AnyStr: ...
