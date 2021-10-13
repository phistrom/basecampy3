# -*- coding: utf-8 -*-
"""
"""

from basecampy3.urls import util
from .recordings import RecordingEndpointURLs


class Todos(RecordingEndpointURLs):
    RECORD_TYPE = "Todo"

    def list_by_todolist(self, project, todolist, status=None, completed=None):
        """
        Return the URL for retrieving To-Do objects from a TodoList ID and a Project ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#get-to-dos

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :param status: active, archived, or trashed to filter out Todos of that type
        :type status: str|None
        :param completed: True or False to filter out Todos that are/aren't checked
        :type completed: bool|None
        :return: a URL for getting a list of To-Dos
        :rtype: basecampy3.urls.URL
        """
        completed = util.boolparam(completed)
        params = {
            "status": status,
            "completed": completed,
        }

        return self._get("/buckets/{project}/todolists/{todolist}/todos.json",
                         project=project, todolist=todolist, params=params)

    def get(self, project, to_do):
        """
        Return a To-do item given a project and a To-do ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#get-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :return: a URL for getting just a single To-do object
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/todos/{to_do}.json",
                         project=project, to_do=to_do)

    def create(self, project, todolist):
        """
        Create a new To-do item in the given To-do List.

        :param project: the ID of a project
        :type project: int
        :param todolist: the ID of a To-do list
        :type todolist: int
        :return: the URL to POST to
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/todolists/{todolist}/todos.json",
                          project=project, todolist=todolist)

    def update(self, project, to_do):
        """
        Update a To-do item in the given project.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#update-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :return: a URL for updating a To-do item
        :rtype: basecampy3.urls.URL
        """

        return self._put("/buckets/{project}/todos/{to_do}.json",
                         project=project, to_do=to_do)

    def complete(self, project, to_do):
        """
        Mark a To-do item complete.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#complete-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :return: a URL for marking a To-do item complete
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/todos/{to_do}/completion.json", project=project, to_do=to_do)

    def uncomplete(self, project, to_do):
        """
        Uncheck a To-do item.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#uncomplete-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :return: a URL for marking a To-do item as not complete
        :rtype: basecampy3.urls.URL
        """

        return self._delete("/buckets/{project}/todos/{to_do}/completion.json", project=project, to_do=to_do)

    def reposition(self, project, to_do):
        """
        Reposition a To-do item.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#reposition-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :return: a URL for repositioning a To-do item
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/todos/{to_do}/position.json", project=project, to_do=to_do)
