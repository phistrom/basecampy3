"""
To-do Sets
https://github.com/basecamp/bc3-api/blob/master/sections/todosets.md

There's one of these per project. All to-do list objects are children of the project's
To-do Set.

The To-Do hierarchy can be confusing.

TodoSet -> TodoLists -> TodoListGroups -> TodoItems
   ^
You are here.
"""

from . import _base, projects, util
from .. import constants


class TodoSet(_base.BasecampObject):
    def create(self, name, description=None):
        """
        Create a new TodoList object in this Project.

        :param name: the name for this TodoList
        :param description: (optional) an HTML-formatted description of this TodoList
        :return: the newly created TodoList
        :rtype: basecampy3.endpoints.todolists.TodoList
        """
        return self._endpoint._api.todolists.create(name=name, description=description, todoset=self)

    def list(self):
        """
        :return: a list of the TodoList objects in this Project
        :rtype: collections.Iterable[basecampy3.endpoints.todolists.TodoList]
        """
        return self._endpoint._api.todolists.list(todoset=self)


class TodoSets(_base.BasecampEndpoint):
    OBJECT_CLASS = TodoSet

    GET_URL = "{base_url}/buckets/{project_id}/todosets/{todoset_id}.json"

    def get(self, project, todoset=None):
        """
        Get a TodoSet object either from a project ID and a todoset ID or just a Project object.

        :param project: a Project object or ID
        :type project: projects.Project|int
        :param todoset: a TodoSet object or ID
        :type todoset: TodoSet|int
        :return: a TodoSet object
        :rtype: TodoSet
        """
        project_id, todoset_id = util.project_or_object(project, todoset, section_name=constants.DOCK_NAME_TODOS)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, todoset_id=todoset_id)
        return self._get(url)
