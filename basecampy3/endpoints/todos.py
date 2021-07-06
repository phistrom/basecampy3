"""
To-Do Items
https://github.com/basecamp/bc3-api/blob/master/sections/todos.md

Individual checkboxes in a TodoList or TodoListGroup object.

The To-Do hierarchy can be confusing.

TodoSet -> TodoLists -> TodoListGroups -> TodoItems
                                             ^
                                        You are here.
"""

from . import recordings, util
import six


class TodoItem(recordings.Recording):
    def check(self):
        """
        Mark this TodoItem as complete.
        """
        self._endpoint.complete(todoitem=self, project=self.project_id)

    def uncheck(self):
        """
        Mark this TodoItem as incomplete.
        """
        self._endpoint.uncomplete(todoitem=self, project=self.project_id)

    def reposition(self, position):
        """
        Change the position of this TodoItem in the TodoList. 1 will put it at the top of the list.

        :param position: the new position for this TodoItem in the list. Must be greater than or equal to 1.
        :type position: int
        """
        self._endpoint.reposition(position=position, todoitem=self, project=self.project_id)

    def save(self, notify=None):
        """
        Saves the fields in this TodoItem using the update method in the Todos endpoint.

        :param notify: whether or not to notify subscribers of the changes
        :type notify: bool
        """
        self._endpoint.update(todoitem=self, project=self.project_id, content=self.content,
                              description=self.description, assignee_ids=self.assignees,
                              completion_subscriber_ids=self.completion_subscribers, notify=notify,
                              due_on=self.due_on, starts_on=self.starts_on)

    def __str__(self):
        try:
            return "[{complete}] '{title}'".format(complete="X" if self.completed else " ", title=self.title)
        except Exception:
            return super(TodoItem, self).__str__()

    def __repr__(self):
        try:
            return "TodoItem('{0.title}', completed={0.completed})"
        except Exception:
            return super(TodoItem, self).__repr__()


class Todos(recordings.RecordingEndpoint):
    OBJECT_CLASS = TodoItem
    LIST_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/todos.json"
    GET_URL = "{base_url}/buckets/{project_id}/todos/{todo_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/todolists/{todolist_id}/todos.json"
    UPDATE_URL = "{base_url}/buckets/{project_id}/todos/{todo_id}.json"

    COMPLETE_URL = "{base_url}/buckets/{project_id}/todos/{todo_id}/completion.json"
    UNCOMPLETE_URL = "{base_url}/buckets/{project_id}/todos/{todo_id}/completion.json"
    REPOSITION_URL = "{base_url}/buckets/{project_id}/todos/{todo_id}/position.json"

    def list(self, todolist, project=None, status=None, completed=False):
        """
        Retrieve a list of the TodoItem objects in the given TodoList.

        :param todolist: a TodoList object or ID
        :type todolist: basecampy3.endpoints.todolists.TodoList|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param status: set this to "archived" or "trashed" for only TodoItems that match that status
        :type status: str
        :param completed: set to True to only get TodoItems that have been completed, by default only incomplete tasks
                          are listed. There is no way to return all Todos (complete and incomplete) at the same time.
        :type completed: bool
        :return: a generator of TodoItem objects in the TodoList specified
        :rtype: collections.Iterable[TodoItem]
        """
        project_id, todolist_id = util.project_or_object(project, todolist)
        params = {}
        if status is not None:
            params['status'] = status
        if completed is not False:
            # if completed is 'true' (case-sensitive), will return completed TodoItems
            # literally any other string (*empty*, 't', 'y', 'false', 'your momma', 'True') returns incomplete tasks
            params['completed'] = six.text_type(completed).lower()  # convert True to 'true'
        url = self.LIST_URL.format(base_url=self.url, todolist_id=todolist_id, project_id=project_id)
        return self._get_list(url, params=params)

    def get(self, todoitem, project=None):
        """
        Get a TodoItem by its ID and project ID.

        :param todoitem: a TodoItem object or ID
        :type todoitem: TodoItem|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :return: a TodoItem
        :rtype: TodoItem
        """
        project_id, todo_id = util.project_or_object(project, todoitem)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, todo_id=todo_id)
        return self._get(url)

    def create(self, content, todolist, project=None, description="", assignee_ids=None,
               completion_subscriber_ids=None, notify=False, due_on=None, starts_on=None):
        """
        Create a new TodoItem in the given TodoList and Project. A TodoList ID and Project ID must be given or just a
        TodoList object. All other parameters are optional.

        :param content: the title or main line of this TodoItem
        :type content: str
        :param todolist: a TodoList object or ID that this TodoItem belongs to
        :type todolist: basecampy3.endpoints.todolists.TodoList|int
        :param project: a Project object or ID that this TodoItem belongs to
        :type project: basecampy3.endpoints.projects.Project|int
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
        :rtype: TodoItem
        """
        project_id, todolist_id = util.project_or_object(project, todolist)
        url = self.CREATE_URL.format(base_url=self.url, project_id=project_id, todolist_id=todolist_id)
        data = {
            "content": content,
            "description": description,
            "notify": notify,
        }
        if assignee_ids is not None:
            data['assignee_ids'] = [int(person) for person in assignee_ids]
        if completion_subscriber_ids is not None:
            data['completion_subscriber_ids'] = [int(person) for person in completion_subscriber_ids]
        if due_on is not None:
            data['due_on'] = self._normalize_date(due_on)
        if starts_on is not None:
            data['starts_on'] = self._normalize_date(starts_on)
        return self._create(url, data=data)

    def update(self, todoitem, project=None, content=False, description=False, assignee_ids=False,
               completion_subscriber_ids=False, notify=None, due_on=False, starts_on=False):
        """
        :param todoitem: a TodoItem object or ID
        :type todoitem: TodoItem|int
        :param project: a Project object or ID that this TodoItem belongs to
        :type project: basecampy3.endpoints.projects.Project|int
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
        """
        project_id, todo_id = util.project_or_object(project, todoitem)
        url = self.UPDATE_URL.format(base_url=self.url, project_id=project_id, todo_id=todo_id)
        if content is False and description is False and assignee_ids is False and completion_subscriber_ids is False \
                and notify is None and due_on is False and starts_on is False:
            raise ValueError("Nothing about this TodoItem would be modified.")
        data = {}
        if content is not False:
            data['content'] = content
        if description is not False:
            data['description'] = description
        if assignee_ids is not False:
            data['assignee_ids'] = assignee_ids
        if completion_subscriber_ids is not False:
            data['completion_subscriber_ids'] = completion_subscriber_ids
        if notify is not None:
            data['notify'] = notify
        if due_on is not False:
            data['due_on'] = self._normalize_date(due_on)
        if starts_on is not False:
            data['starts_on'] = self._normalize_date(starts_on)

        return self._update(url, data)

    def complete(self, todoitem, project=None):
        """
        Mark a TodoItem as complete (check its box).

        :param todoitem: a TodoItem object or ID
        :type todoitem: TodoItem|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        """
        project_id, todo_id = util.project_or_object(project, todoitem)
        url = self.COMPLETE_URL.format(base_url=self.url, project_id=project_id, todo_id=todo_id)

        self._no_response(url, method="POST")

    def uncomplete(self, todoitem, project=None):
        """
        Mark a TodoItem as not complete (un-check its box).

        :param todoitem: a TodoItem object or ID
        :type todoitem: TodoItem|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        """
        project_id, todo_id = util.project_or_object(project, todoitem)
        url = self.UNCOMPLETE_URL.format(base_url=self.url, project_id=project_id, todo_id=todo_id)

        self._no_response(url, method="DELETE")

    def reposition(self, position, todoitem, project=None):
        """
        Moves the TodoItem up or down the list. A position of 1 puts it at the top.

        :param position: the new position for this TodoItem as an integer greater than or equal to 1
        :type position: int
        :param todoitem: a TodoItem object or ID
        :type todoitem: TodoItem|int
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        """
        project_id, todo_id = util.project_or_object(project, todoitem)
        data = {'position': position}
        url = self.REPOSITION_URL.format(base_url=self.url, project_id=project_id, todo_id=todo_id)

        self._no_response(url, data=data)

    @staticmethod
    def _normalize_date(somedate):
        """
        Take a date or datetime and turn them into the string YYYY-MM-DD. If `somedate` is None, returns an
        empty string.

        :param somedate: the date to be coerced into a YYYY-MM-DD format
        :type somedate: datetime.date|datetime.datetime|str
        :return: a string in the format YYYY-MM-DD
        :rtype: str
        """
        if somedate is None:
            return ""

        try:
            somedate = somedate.strftime("%Y-%m-%d")
        except AttributeError:
            pass

        return somedate
