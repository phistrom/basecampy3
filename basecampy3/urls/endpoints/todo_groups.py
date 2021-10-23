# -*- coding: utf-8 -*-
"""
URLs related to To-do Group objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs
from .. import util


class TodoGroups(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md
    https://3.basecamp-help.com/article/48-to-dos#group-to-dos
    """

    RECORD_TYPE = "Todolist"

    def list_by_todolist(self, project, todolist, status=None, completed=None, **kwargs):
        """
        Get a list of To-do Groups in the given To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#list-to-do-list-groups

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :param status: archived or trashed for filtering
        :type status: str|None
        :param completed: if True, return only completed To-do Items
        :type completed: bool|None
        :param kwargs: additional query string parameters (for future use)
        :type kwargs: str
        :return: the URL for getting a list of To-do Groups in the desired To-do List
        :rtype: basecampy3.urls.URL
        """
        kwargs["status"] = status
        if completed is not None:
            # must use strings for query string params
            kwargs["completed"] = "true" if completed else "false"
        kwargs = util.filter_unused(kwargs)

        return self._get("/buckets/{project}/todolists/{todolist}/groups.json",
                         project=project, todolist=todolist, params=kwargs)

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

    def create(self, project, todolist, name, **kwargs):
        """
        Create a new To-do Group in the given To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#create-a-to-do-list-group

        :param project: the ID of a Project
        :type project: int
        :param todolist: the ID of a To-do List
        :type todolist: int
        :param name: the name of this To-do Group
        :type name: typing.AnyStr
        :param kwargs: additional JSON parameters (unused at this time)
        :type kwargs: typing.Any
        :return: the URL for creating new To-do Groups in the desired To-do List
        :rtype: basecampy3.urls.URL
        """
        kwargs["name"] = name
        kwargs = util.filter_unused(kwargs)

        return self._post("/buckets/{project}/todolists/{todolist}/groups.json",
                          project=project, todolist=todolist, json_dict=kwargs)

    def reposition(self, project, todogroup, position, **kwargs):
        """
        Move a To-do List Group up or down in order on the To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md#reposition-a-to-do-list-group

        :param project: the ID of a Project
        :type project: int
        :param todogroup: the ID of a To-do Group
        :type todogroup: int
        :param position: the new position (must be 0 or up)
        :type position: int
        :param kwargs: additional JSON paramters (for future use)
        :type kwargs: typing.Any
        :return: the URL for repositioning a To-do Group
        :rtype: basecampy3.urls.URL
        """

        kwargs["position"] = position

        kwargs = util.filter_unused(kwargs)

        return self._put("/buckets/{project}/todolists/groups/{todogroup}/position.json",
                         project=project, todogroup=todogroup, json_dict=kwargs)
