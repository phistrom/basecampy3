# -*- coding: utf-8 -*-
"""
URLs related to To-do List objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs
from .. import util


class TodoLists(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md
    https://3.basecamp-help.com/article/48-to-dos
    """

    RECORD_TYPE = "Todolist"

    def list_by_todoset(self, project, todo_set, status=None, **kwargs):
        """
        Get To-do Lists in the given To-do Set.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-to-do-lists

        :param project: the ID of a Project
        :type project: int
        :param todo_set: the ID of a To-do Set
        :type todo_set: int
        :param status: archived or trashed for filtering
        :type status: str|None
        :param kwargs: additional query string parameters (for future use)
        :type kwargs: str
        :return: the URL for listing the To-do Lists in the desired To-do Set
        :rtype: basecampy3.urls.URL
        """

        kwargs["status"] = status
        kwargs = util.filter_unused(kwargs)

        return self._get("/buckets/{project}/todosets/{todo_set}/todolists.json",
                         project=project, todo_set=todo_set, params=kwargs)

    def get(self, project, todolist):
        """
        Get a To-do List by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-a-to-do-list

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :return: the URl for retrieving the desired To-do List
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/todolists/{todolist}.json",
                         project=project, todolist=todolist)

    def create(self, project, todo_set, name, description=None, **kwargs):
        """
        Create a new To-do List in the given To-do Set.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#create-a-to-do-list

        :param project: the ID of a Project
        :type project: int
        :param todo_set: the ID of a To-do Set
        :type todo_set: int
        :param name: the name for this new TodoList
        :type name: typing.AnyStr
        :param description: an optional rich-text (HTML) description
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (not currently used)
        :type kwargs: typing.Any
        :return: the URL for creating a new To-do List in the desired To-do Set
        :rtype: basecampy3.urls.URL
        """

        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._post("/buckets/{project}/todosets/{todo_set}/todolists.json",
                          project=project, todo_set=todo_set, json_dict=kwargs)

    def update(self, project, todolist, name=None, description=None, **kwargs):
        """
        Update a To-do List's name and/or description.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#update-a-to-do-list

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :param name: a new name for this TodoList
        :type name: typing.AnyStr|None
        :param description: a new description for this TodoList
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (not currently used)
        :return: the URL for modifying the desired To-do List
        :rtype: basecampy3.urls.URL
        """

        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._put("/buckets/{project}/todolists/{todolist}.json",
                         project=project, todolist=todolist, json_dict=kwargs)
