"""
To-Do Lists
https://github.com/basecamp/bc3-api/blob/master/sections/todolists.md

Lists of TodoItems and TodoListGroups under a TodoSet.

The To-Do hierarchy can be confusing.

TodoSet -> TodoLists -> TodoListGroups -> TodoItems
              ^
        You are here.
"""

import abc
import six
from . import recordings, todosets, util
from .. import constants


@six.add_metaclass(abc.ABCMeta)
class TodoCollection(recordings.Recording):
    """
    Base class for collections of TodoItems like TodoLists and TodoListGroups.
    """

    def list(self, status=None, completed=False):
        """
        Returns an iterable of all Todos directly under this TodoList. Use the TodoList.list_groups function to
        get TodoListGroups, and then call the list function on those TodoListGroups to get the Todos nested under them.

        :param status: set this to "archived" or "trashed" for only TodoItems that match that status
        :type status: str
        :param completed: set to True to only get TodoItems that have been completed, by default only incomplete tasks
                          are listed. There is no way to return all Todos (complete and incomplete) at the same time.
        :type completed: bool
        :return: a generator of TodoItem objects in this TodoList
        :rtype: collections.abc.Iterable[basecampy3.endpoints.todos.TodoItem]
        """
        return self._endpoint._api.todos.list(todolist=self, project=self.project_id,
                                              status=status, completed=completed)


class TodoList(TodoCollection):
    @property
    def todoset_id(self):
        """
        :return: the ID of the TodoSet that this TodoList belongs to
        :rtype: int
        """
        return int(self._values['parent']['id'])

    def create(self, content, description="", assignee_ids=None, completion_subscriber_ids=None, notify=False,
               due_on=None, starts_on=None):
        """
        Create a new TodoItem in the given TodoList and Project. A TodoList ID and Project ID must be given or just a
        TodoList object. All other parameters are optional.

        :param content: the title or main line of this TodoItem
        :type content: str
        :param description: a longer, HTML-formatted text about this TodoItem
        :type description: str
        :param assignee_ids: a list of Person objects or just their IDs that are responsible for this TodoItem
        :type assignee_ids: list[basecampy3.endpoints.people.Person|int]
        :param completion_subscriber_ids: a list of Person objects or just their IDs that will be notified when this
                                          TodoItem is marked completed
        :type completion_subscriber_ids: list[basecampy3.endpoints.people.Person|int]
        :param notify: set to True if you want assignees to be notified
        :type notify: bool
        :param due_on: the date this item is due. Must be a YYYY-MM-DD string, or a date or datetime object
        :type due_on: str|datetime.datetime|datetime.date
        :param starts_on: the date this item starts. Must be a YYYY-MM-DD string, or a date or datetime object
        :type starts_on: str|datetime.datetime|datetime.date
        :return: the newly created TodoItem
        :rtype: basecampy3.endpoints.todos.TodoItem
        """
        return self._endpoint._api.todos.create(content=content, description=description, assignee_ids=assignee_ids,
                                                completion_subscriber_ids=completion_subscriber_ids, notify=notify,
                                                due_on=due_on, starts_on=starts_on, todolist=self,
                                                project=self.project_id)

    def create_group(self, name):
        """
        Create a new TodoListGroup in this TodoList.

        :param name: the name to give this TodoListGroup
        :type name: str
        :return: the newly created TodoListGroup object
        :rtype: basecampy3.endpoints.todolist_groups.TodoListGroup
        """
        return self._endpoint._api.todolist_groups.create(name=name, todolist=self, project=self.project_id)

    def list_groups(self, status=None):
        """
        List the TodoListGroups under this TodoList. TodoListGroups are a grouping of 0 or more TodoItems with a title.

        :param status: set this to "archived" or "trashed" for only TodoListGroups that match that status
        :type status: str
        :return: a generator of TodoListGroup objects in this TodoList
        :rtype: collections.abc.Iterable[basecampy3.endpoints.todolist_groups.TodoListGroup]
        """
        return self._endpoint._api.todolist_groups.list(todolist=self, project=self.project_id, status=status)

    def __str__(self):
        try:
            return "'{name}'".format(name=self.name)
        except Exception:
            return super(TodoList, self).__str__()


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
