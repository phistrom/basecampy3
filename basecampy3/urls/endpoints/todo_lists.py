# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class TodoLists(EndpointURLs):
    def list(self, project, todo_set, status=None, **kwargs):
        """
        Get To-do Lists in the given To-do Set.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#get-to-do-lists

        :param project: the ID of a Project
        :type project: int
        :param todo_set: the ID of a To-do Set
        :type todo_set: int
        :param status: active, archived, or trashed for filtering
        :type status: str|None
        :param kwargs: additional query string parameters
        :type kwargs: str
        :return: the URL for listing the To-do Lists in the desired To-do Set
        :rtype: basecampy3.urls.URL
        """
        params = {
            "status": status,
        }
        params.update(kwargs)

        return self._get("/buckets/{project}/todosets/{todo_set}/todolists.json",
                         project=project, todo_set=todo_set, params=params)

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

    def create(self, project, todo_set):
        """
        Create a new To-do List in the given To-do Set.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#create-a-to-do-list

        :param project: the ID of a Project
        :type project: int
        :param todo_set: the ID of a To-do Set
        :type todo_set: int
        :return: the URL for creating a new To-do List in the desired To-do Set
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/todosets/{todo_set}/todolists.json",
                          project=project, todo_set=todo_set)

    def update(self, project, todolist):
        """
        Update a To-do List's name and/or description.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md#update-a-to-do-list

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :return: the URL for modifying the desired To-do List
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/todolists/{todolist}.json",
                         project=project, todolist=todolist)
