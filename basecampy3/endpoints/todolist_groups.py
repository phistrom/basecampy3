from . import _base, projects, todolists, util


class TodoListGroup(_base.BasecampObject):
    pass


class TodoListGroups(_base.BasecampEndpoint):
    OBJECT_CLASS = TodoListGroup

    LIST_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/groups.json"
    GET_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_group_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/groups.json"
    REPOSITION_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_group_id}.json"

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

    def reposition(self, position, todolist, project=None):
        """
        Reposition a TodoListGroup in a TodoList.

        :param position: the new position as an integer greater than or equal to 1
        :type position: int
        :param todolist: a TodoList object or ID
        :type todolist: todolists.TodoList|int
        :param project: a Project object or ID
        :type project: projects.Project|int
        """
        project_id, todolist_id = util.project_or_object(project, todolist)
        data = {"position": position}
        url = self.REPOSITION_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        self._update(url, data=data)
