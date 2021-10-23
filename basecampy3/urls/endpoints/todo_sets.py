# -*- coding: utf-8 -*-
"""
URLs related to To-do Set objects in the Basecamp 3 API.
"""

from .base import EndpointURLs


class TodoSets(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/todosets.md
    https://3.basecamp-help.com/article/48-to-dos
    """
    def get(self, project, todo_set):
        """
        Get a TodoSet, the highest level in the Todos hierarchy.

        https://github.com/basecamp/bc3-api/blob/master/sections/todosets.md#get-to-do-set

        :param project: the project the TodoSet is in (either Basecampy object
                        or the Project ID integer)
        :type project: basecampy3.endpoints.projects.Project|int
        :param todo_set: the TodoSet ID or Basecampy object
        :type todo_set: basecampy3.endpoints.todo_sets.TodoSet|int
        :return: the URL to retrieve the desired TodoSet
        :rtype: basecampy3.urls.URL
        """

        return self._get("/buckets/{project}/todosets/{todo_set}.json",
                         project=project, todo_set=todo_set)
