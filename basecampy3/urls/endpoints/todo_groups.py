# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class TodoGroups(EndpointURLs):
    def list(self, project, todolist, status=None, **kwargs):
        """
        Get a list of To-do Groups in the given To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#list-to-do-list-groups

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :param status: active, archived, or trashed for filtering
        :type status: str|None
        :param kwargs: additional query string parameters
        :type kwargs: str
        :return: the URL for getting a list of To-do Groups in the desired To-do List
        :rtype: basecampy3.urls.URL
        """

        params = {
            "status": status,
        }
        params.update(kwargs)

        return self._get("/buckets/{project}/todolists/{todolist}/groups.json",
                         project=project, todolist=todolist, params=params)

    def get(self, project, todogroup):
        """
        Get a To-do Group by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#get-a-to-do-list-group

        :param project: the ID of a Project
        :type project: int
        :param todogroup: the ID of a To-do Group
        :type todogroup: int
        :return: the URL for retrieving the desired To-do Group
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/todolists/{todogroup}.json",
                         project=project, todogroup=todogroup)

    def create(self, project, todolist):
        """
        Create a new To-do Group in the given To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#create-a-to-do-list-group

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :return: the URL for creating new To-do Groups in the desired To-do List
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/todolists/{todolist}/groups.json",
                          project=project, todolist=todolist)

    def reposition(self, project, todogroup):
        """
        Move a To-do List Group up or down in order on the To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#reposition-a-to-do-list-group

        :param project: the ID of a Project
        :type project: int
        :param todogroup: the ID of a To-do Group
        :type todogroup: int
        :return: the URL for repositioning a To-do Group
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/todolists/groups/{todogroup}/position.json",
                         project=project, todogroup=todogroup)
