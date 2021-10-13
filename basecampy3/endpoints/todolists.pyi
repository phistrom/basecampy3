import datetime
from typing import Iterable, Literal, Optional, TypedDict, Union

from . import people, recordings, todos, todolist_groups, util
from .. import constants


class TodoCollection(recordings.Recording):
    def list(self, status: Optional[str], completed: bool) -> Iterable[todos.TodoItem]: ...


StatusString = Literal["active", "archived", "trashed"]


class ParentDict(TypedDict):
    id: int
    title: str
    type: Literal["Todoset"]
    url: str
    app_url: str


class ProjectDict(TypedDict):
    id: int
    name: str
    type: Literal["Project"]


class CompanyDict(TypedDict):
    id: int
    name: str


class CreatorDict(TypedDict):
    id: int
    attachable_sgid: str
    name: str
    email_address: str
    personable_type: str
    title: str
    bio: Optional[str]
    created_at: str
    updated_at: str
    admin: bool
    owner: bool
    client: bool
    time_zone: str
    avatar_url: str
    company: CompanyDict


class TodoList(TodoCollection):
    id: int
    status: StatusString
    visible_to_clients: bool
    created_at: str
    updated_at: str
    title: str
    inherits_status: bool
    type: Literal["Todolist"]
    url: str
    app_url: str
    bookmark_url: str
    subscription_url: str
    comments_count: int
    comments_url: str
    position: int
    parent: ParentDict
    bucket: ProjectDict
    creator: CreatorDict
    description: str
    completed: bool
    completed_ratio: str
    name: str
    todos_url: str
    groups_url: str
    app_todos_url: str


    @property
    def todoset_id(self) -> int: ...

    def create(self, content: str, description: Optional[str],
               assignee_ids: Optional[Iterable[Union[people.Person, int]]],
               completion_subscriber_ids: Optional[Iterable[Union[people.Person, int]]],
               notify: bool, due_on: Optional[Union[str, datetime.datetime, datetime.date]],
               starts_on: Optional[Union[str, datetime.datetime, datetime.date]]) -> todos.TodoItem: ...

    def create_group(self, name: str) -> todolist_groups.TodoListGroup: ...

    def list_groups(self, status: Optional[StatusString]) -> \
            Iterable[todolist_groups.TodoListGroup]: ...


class TodoLists(recordings.RecordingEndpoint):
    OBJECT_CLASS = TodoList

    LIST_URL = "{base_url}/buckets/{project_id}/todosets/{todoset_id}/todolists.json"
    GET_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/todosets/{todoset_id}/todolists.json"
    UPDATE_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}.json"

    def list(self, project=None, todoset=None, status=None):
        """
        Get a list of TodoList objects. Requires either a Project object or a project ID with a TodoSet ID.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project
        :param todoset: a TodoSet object or ID
        :type todoset: todosets.TodoSet
        :param status: (optional) get TodoLists that are "archived" or "trashed"
        :type status: str
        :return: a list of TodoList objects from the given Project
        :rtype: collections.Iterable[TodoList]
        """
        params = {}
        if status is not None:
            params['status'] = status
        project_id, todoset_id = util.project_or_object(project, todoset, section_name=constants.DOCK_NAME_TODOS)
        url = self.LIST_URL.format(base_url=self.url, project_id=project_id, todoset_id=todoset_id)
        return self._get_list(url, params=params)

    def get(self, todolist, project=None):
        """
        Get a TodoList by its ID and a Project's ID or just a TodoList object.

        :param todolist: a TodoList object or ID
        :type todolist: TodoList|int
        :param project: a Project object or ID (optional if `todolist` is an object)
        :type project: basecampy3.endpoints.projects.Project|int
        :return: a TodoList object
        :rtype: TodoList
        """
        project_id, todolist_id = util.project_or_object(project, todolist)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        return self._get(url)

    def create(self, name, description=None, project=None, todoset=None):
        """
        Create a new TodoList in the given Project.

        :param name: the name for this TodoList
        :type name: str
        :param description:
        :type description: str
        :param project:
        :type project: basecampy3.endpoints.projects.Project|int
        :param todoset:
        :type todoset: todosets.TodoSet|int
        :return: a new TodoList object
        :rtype: TodoList
        """
        project_id, todoset_id = util.project_or_object(project, todoset, section_name=constants.DOCK_NAME_TODOS)
        data = {
            "name": name,
            "description": description
        }
        url = self.CREATE_URL.format(base_url=self.url, project_id=project_id, todoset_id=todoset_id)
        return self._create(url, data=data)

    def update(self, todolist, project=None, name=False, description=False):
        if name is False and description is False:
            raise ValueError("Nothing to update for TodoList %s" % todolist)
        project_id, todolist_id = util.project_or_object(project, todolist)
        data = {}
        if name is not False:
            data['name'] = name
        if description is not False:
            data['description'] = description
        url = self.UPDATE_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        return self._update(url, data=data)
