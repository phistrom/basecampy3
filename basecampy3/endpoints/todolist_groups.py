"""
To-Do List Groups
https://github.com/basecamp/bc3-api/blob/master/sections/todolist_groups.md

Subgroups of TodoItems within a TodoList.

The To-Do hierarchy can be confusing.

TodoSet -> TodoLists -> TodoListGroups -> TodoItems
                             ^
                        You are here.
"""

from . import projects, recordings, todolists, util


class TodoListGroup(todolists.TodoCollection):
    def reposition(self, position):
        """
        Change the position of this TodoItem in the TodoList. 1 will put it at the top of the list.

        :param position: the new position for this TodoItem in the list. Must be greater than or equal to 1.
        :type position: int
        """
        self._endpoint.reposition(position=position, todolist_group=self, project=self.project_id)

    def __str__(self):
        try:
            return "'{}'".format(self.name)
        except Exception:
            return super(TodoListGroup, self).__str__()

    def __repr__(self):
        try:
            return "TodoListGroup('{}')".format(self.name)
        except Exception:
            return super(TodoListGroup, self).__repr__()


class TodoListGroups(recordings.RecordingEndpoint):
    OBJECT_CLASS = TodoListGroup

    LIST_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/groups.json"
    GET_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_group_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/groups.json"
    REPOSITION_URL = "{base_url}/buckets/{project_id}/todolists/groups/{todolist_group_id}/position.json"

    def list(self, todolist, project=None, status=None):
        """
        Retrieves a list of TodoListGroup objects from a given TodoList. Requires either a TodoList object or a
        project ID with a TodoList ID.

        :param todolist: a TodoList object or ID
        :type todolist: todolists.TodoList|int
        :param project: a Project object or ID
        :type project: projects.Project|int
        :param status: (optional) can use "archived" or "trashed" to get only TodoListGroups of that type
        :type status: str
        :return: a list of TodoListGroup objects
        :rtype: collections.Iterable[TodoListGroup]
        """
        params = {}
        if status is not None:
            params['status'] = status
        project_id, todolist_id = util.project_or_object(project, todolist)
        url = self.LIST_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        return self._get_list(url, params=params)

    def get(self, todolist_group, project=None):
        """
        Return a TodoListGroup given a TodoListGroup object or a Project ID and a TodoListGroup ID
        :param todolist_group: a TodoListGroup object or ID
        :type todolist_group: TodoListGroup|int
        :param project:
        :type project: projects.Project|int
        :return:
        """
        project_id, todolist_group_id = util.project_or_object(project, todolist_group)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, todolist_group_id=todolist_group_id)
        return self._get(url)

    def create(self, name, todolist, project=None):
        """
        Create a new TodoListGroup in the given TodoList in the given Project.

        :param name: the name of the new group
        :type name: str
        :param todolist: a TodoList object or ID
        :type todolist: todolists.TodoList|int
        :param project: a Project object or ID
        :type project: projects.Project|int
        :return: a new TodoListGroup object
        :rtype: TodoListGroup
        """
        project_id, todolist_id = util.project_or_object(project, todolist)
        data = {"name": name}
        url = self.CREATE_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        return self._create(url, data=data)

    def reposition(self, position, todolist_group, project=None):
        """
        Reposition a TodoListGroup in a TodoList.

        :param position: the new position as an integer greater than or equal to 1
        :type position: int
        :param todolist_group: a TodoListGroup object or ID
        :type todolist_group: TodoListGroup|int
        :param project: a Project object or ID
        :type project: projects.Project|int
        """
        project_id, todolist_group_id = util.project_or_object(project, todolist_group)
        data = {"position": position}
        url = self.REPOSITION_URL.format(base_url=self.url, project_id=project_id, todolist_group_id=todolist_group_id)
        self._no_response(url, data=data)
