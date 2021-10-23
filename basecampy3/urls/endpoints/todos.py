# -*- coding: utf-8 -*-
"""
URLs related to To-do Item objects in the Basecamp 3 API.
"""

from basecampy3.urls import util
from .recordings import RecordingEndpointURLs
import datetime

_omit = object()


class Todos(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/todos.md
    https://3.basecamp-help.com/article/48-to-dos
    """
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

    def create(self, project, todolist, content, description=None,
               assignee_ids=None, completion_subscriber_ids=None, notify=None,
               due_on=None, starts_on=None, **kwargs):
        """
        Create a new To-do item in the given To-do List.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#create-a-to-do

        :param project: the ID of a project
        :type project: int
        :param todolist: the ID of a To-do list
        :type todolist: int
        :param content: what this To-do item is all about
        :type content: typing.AnyStr
        :param description: rich text (HTML) description for additional info
        :type description: typing.AnyStr|None
        :param assignee_ids: a list of people assigned to this To-do item
                             (can be a mix of Basecampy People objects or
                             Person ID integers in an iterable)
        :type assignee_ids: list[basecampy3.endpoints.people.Person|int]|None
        :param completion_subscriber_ids: a list of people to be notified upon
                                          completion of the To-do item
        :type completion_subscriber_ids: list[basecampy3.endpoints.people.Person|int]|None
        :param notify: whether to notify assignees about being assigned to
                       this To-do item
        :type notify: bool|None
        :param due_on: a date when this To-do should be completed by
        :type due_on: datetime.date|datetime.datetime|typing.AnyStr
        :param starts_on: allows the to-do to run from this date to the
                          `due_on` date
        :type starts_on: datetime.date|datetime.datetime|typing.AnyStr
        :param kwargs: additional JSON parameters (no currently used)
        :type kwargs: typing.Any
        :return: the URL for creating a new To-do item
        :rtype: basecampy3.urls.URL
        """
        args = self._create_or_update(
            content=content,
            description=description,
            assignee_ids=assignee_ids,
            completion_subscriber_ids=completion_subscriber_ids,
            notify=notify,
            due_on=due_on,
            starts_on=starts_on
        )

        kwargs.update(args)

        kwargs = util.filter_unused(kwargs)

        return self._post("/buckets/{project}/todolists/{todolist}/todos.json",
                          project=project, todolist=todolist, json_dict=kwargs)

    def update(self, project, to_do, content, description=None,
               assignee_ids=None, completion_subscriber_ids=None,
               notify=None, due_on=None, starts_on=None, **kwargs):
        """
        Update a To-do item in the given project. Warning! Any omitted
        parameter causes that parameter to be cleared. Please read the API
        docs for this endpoint!

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#update-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :param content: change what this To-do item is all about
        :type content: typing.AnyStr
        :param description: new rich text (HTML) description
        :type description: typing.AnyStr|None
        :param assignee_ids: a list of people assigned to this To-do item
                             (can be a mix of Basecampy People objects or
                             Person ID integers in an iterable)
        :type assignee_ids: list[basecampy3.endpoints.people.Person|int]|None
        :param completion_subscriber_ids: a list of people to be notified upon
                                          completion of the To-do item
        :type completion_subscriber_ids: list[basecampy3.endpoints.people.Person|int]|None
        :param notify: whether to notify assignees about being assigned to
                       this To-do item
        :type notify: bool|None
        :param due_on: a date when this To-do should be completed by
        :type due_on: datetime.date|datetime.datetime|typing.AnyStr
        :param starts_on: allows the to-do to run from this date to the
                          `due_on` date
        :type starts_on: datetime.date|datetime.datetime|typing.AnyStr
        :param kwargs: additional JSON parameters (for future use)
        :type kwargs: typing.Any
        :return: a URL for updating a To-do item
        :rtype: basecampy3.urls.URL
        """
        args = self._create_or_update(
            content=content,
            description=description,
            assignee_ids=assignee_ids,
            completion_subscriber_ids=completion_subscriber_ids,
            notify=notify,
            due_on=due_on,
            starts_on=starts_on
        )
        kwargs.update(args)

        return self._put("/buckets/{project}/todos/{to_do}.json",
                         project=project, to_do=to_do, json_dict=kwargs)

    @staticmethod
    def _create_or_update(content, description=None, assignee_ids=None,
                          completion_subscriber_ids=None, notify=None,
                          due_on=None, starts_on=None):
        args = {
            "content": content,
            "description": description,
            "assignee_ids": util.to_ids(assignee_ids),
            "completion_subscriber_ids": util.to_ids(completion_subscriber_ids),
            "due_on": util.to_date_string(due_on),
            "starts_on": util.to_date_string(starts_on),
        }

        if notify:
            args["notify"] = True

        return args

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

    def reposition(self, project, to_do, position, **kwargs):
        """
        Reposition a To-do item.

        https://github.com/basecamp/bc3-api/blob/master/sections/todos.md#reposition-a-to-do

        :param project: the ID of a project
        :type project: int
        :param to_do: the ID of a To-do item
        :type to_do: int
        :param position: the new position (must be 0 or up)
        :type position: int
        :param kwargs: additional JSON parameters (for future use)
        :type kwargs: typing.Any
        :return: a URL for repositioning a To-do item
        :rtype: basecampy3.urls.URL
        """

        kwargs["position"] = position
        kwargs = util.filter_unused(kwargs)

        return self._put("/buckets/{project}/todos/{to_do}/position.json",
                         project=project, to_do=to_do, json_dict=kwargs)
