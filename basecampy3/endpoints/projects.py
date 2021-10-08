from . import _base, people, util
from .. import constants
from ..exc import *

import requests
import six

import time


@six.python_2_unicode_compatible
class Project(_base.BasecampObject):
    """
    A Project, also known as a Basecamp, on Basecamp.
    """

    def add_new_user(self, name, email_address, title=None, company_name=None):
        """
        Invite a new user to Basecamp, and add them to this Project. There's no other way to create a new user in
        Basecamp using the API. They must be invited to an initial Project.

        :param name: the user's display name
        :type name: str
        :param email_address: the email address to send the invite to
        :type email_address: str
        :param title: (optional) this user's title at a company
        :type title: str
        :param company_name: (optional) the name of the company this user works at
        :type company_name: str
        :return: the newly created Person object
        :rtype: people.Person
        """
        return self._endpoint.add_new_user(self.id, name=name, email_address=email_address, title=title,
                                           company_name=company_name)

    def modify_access(self, grant=None, revoke=None):
        """
        Change who is allowed to access this Project. `grant` and `revoke` take a list of Person objects or a list of
        Person IDs as integers. They can both be specified at the same time.

        :param grant: a list of Person objects or Person IDs (ints) to grant access
        :type grant: list[people.Person|int]
        :param revoke: a list of Person objects or Person IDs (ints) to remove from the Project
        :type revoke: list[people.Person|int]
        :return: a response object
        :rtype: requests.Response
        """
        return self._endpoint.modify_access(self.id, grant=grant, revoke=revoke)

    def trash(self):
        """
        Trash this project. Trashed projects will be deleted from Basecamp 3 after 30 days.
        """
        self._endpoint.trash(self.id)

    def update(self, name=False, description=False):
        """
        Change this Project's name and/or description.

        :param name: the new name for this Project. A value of False means no change.
        :type name: str
        :param description: the new description for this Project. A value of False means no change.
        :type description: str
        """
        self._endpoint.update(self.id, name=name, description=description)

    @property
    def campfire(self):
        """
        :return: the Campfire object associated with this Project.
        :rtype: basecampy3.endpoints.campfires.Campfire
        """
        section = self._get_dock_section(constants.DOCK_NAME_CAMPFIRE)
        return self._endpoint._api.campfires.get(campfire=section['id'], project=self.id)

    @property
    def message_board(self):
        """
        :return: the MessageBoard object associated with this Project
        :rtype: basecampy3.endpoints.message_boards.MessageBoard
        """
        section = self._get_dock_section(constants.DOCK_NAME_MESSAGE_BOARD)
        return self._endpoint._api.message_boards.get(board=section['id'], project=self.id)

    @property
    def todoset(self):
        """
        :return: the TodoSet object associated with this Project
        :rtype: basecampy3.endpoints.todosets.TodoSet
        """
        section = self._get_dock_section(constants.DOCK_NAME_TODOS)
        return self._endpoint._api.todosets.get(todoset=section['id'], project=self.id)

    @property
    def people(self):
        """
        A list of people who currently have access to this Project.

        :return: a list of Person objects
        :rtype: collections.Iterable[basecampy3.endpoints.people.Person]
        """
        return self._endpoint._api.people.list(project=self.id)

    def list_answers_in_question(self, question):
        """
        A list of answers for question with id

        :param question: the id of question to list answers from
        :type question: int
        :return: a list of Answer objects
        :rtype: collections.Iterable[basecampy3.endpoints.answers.Answer]
        """
        return self._endpoint._api.answers.list(project=self.id, question=question)

    def _get_dock_section(self, name):
        for section in self.dock:
            if section['name'] == name:
                return section

    def __str__(self):
        try:
            return u"Project {0.id}: '{0.name}'".format(self)
        except AttributeError:
            return super(Project, self).__str__()

    def __repr__(self):
        repr_dict = {k: v for k, v in self._values.items() if k not in ("dock",)}
        return "Project(%s)" % repr(repr_dict)


class Projects(_base.BasecampEndpoint):
    OBJECT_CLASS = Project

    CREATE_URL = "{base_url}/projects.json"
    GET_URL = "{base_url}/projects/{project_id}.json"
    LIST_URL = "{base_url}/projects.json"
    MODIFY_ACCESS_URL = "{base_url}/projects/{project_id}/people/users.json"
    TRASH_URL = "{base_url}/projects/{project_id}.json"
    UPDATE_URL = "{base_url}/projects/{project_id}.json"

    CREATION_FROM_TEMPLATE_TIMEOUT = 10

    def add_new_user(self, project, name, email_address, title=None, company_name=None):
        """
        Invite a new user to Basecamp, and add them to the given Project. There's no other way to create a new user in
        Basecamp using the API. They must be invited to an initial Project.

        :param project: a Project object or ID
        :type project: Project|int
        :param name: the user's display name
        :type name: str
        :param email_address: the email address to send the invite to
        :type email_address: str
        :param title: (optional) this user's title at a company
        :type title: str
        :param company_name: (optional) the name of the company this user works at
        :type company_name: str
        :return: the newly created Person object
        :rtype: basecampy3.endpoints.people.Person
        """
        create = {
            'name': name,
            'email_address': email_address,
        }
        if title is not None:
            create['title'] = title
        if company_name is not None:
            create['company_name'] = company_name
        data = {
            'create': [
                create,
            ]
        }

        project = int(project)
        url = self.MODIFY_ACCESS_URL.format(base_url=self.url, project_id=project)
        resp = self._api._session.put(url, json=data)
        result = resp.json()
        new_user = people.Person(json_dict=result['granted'][0], endpoint=self._api.people)
        return new_user

    def create(self, name, description="", template=None):
        """
        Create a new Project on Basecamp

        :param name: the name for this new Project
        :type name: str
        :param description: (optional) a description for this new Project
        :type description: str
        :param template: a Template object or ID
        :type template:  basecampy3.endpoints.templates.Template|int
        :return: the newly created Project object
        :rtype: Project
        """
        if template is not None:
            return self._create_from_template(name, description, template)
        data = {
            'name': name,
            'description': description,
        }
        url = self.CREATE_URL.format(base_url=self.url)
        new_project = self._create(url, data=data)
        return new_project

    def find(self, any_=None, name=None, description=None, status=None, **kwargs):
        """
        Finds Projects by name and/or description. The Basecamp 3 API does not have a search function for Projects so
        this function has to iterate through all projects to search. Bare that in mind when considering the performance
        of this function. Subsequent calls should be faster as they should be cached.

        If `any` is a string, match any project where the name or description or both contain the
        string (case-insensitive).

        If `name`, and/or `description` is a string, a Project is a match if its name contains `name` or
        description contains `description` (case-insensitive).

        `name` and `description` will be ignored if `any` is specified.

        `any`, `name`, or `description` can also be compiled regular expression objects (using re.compile). The search()
        function will be called on the object. Case-sensitivity will depend on your compiled regular expression having
        the re.IGNORECASE flag.

        :param any_: a string or regular expression to match against Project names AND descriptions. If any part of a
                    Project name or description matches the string, it will be considered a match.
        :type any_: str|typing.Pattern
        :param name: a string or regular expression to search project names for
        :type name: str|typing.Pattern
        :param description: a string or regular expression to search project descriptions for
        :type description: str|typing.Pattern
        :param status: can be "archived" or "trashed" to search Projects with that status. By default, only active
                       Projects are searched.
        :type status: str
        :return: a list of Project objects that matched your search terms, sorted by most recently created first (which
                is the behavior of the list projects API call)
        :rtype: list[Project]
        """
        if not any_ and kwargs.get('any'):
            any_ = kwargs.pop('any')
        if not any((any_, name, description)):
            raise ValueError("Must specify at least one search term.")
        if any_:
            # for each parameter, we test for the existence of a search attribute to determine
            # if the parameter is a `re.Pattern` or a string.
            try:
                _ = any_.search  # assignment makes PyCharm not complain
                # we must be dealing with a regex
                name_regex = any_
                name_str = None
                desc_regex = any_
                desc_str = None
            except AttributeError:  # search didn't exist, assume string
                any_upper = any_.upper()
                name_regex = None
                name_str = any_upper
                desc_regex = None
                desc_str = any_upper
        else:
            try:
                _ = name.search
                name_regex = name
                name_str = None
            except AttributeError:  # search didn't exist
                name_regex = None
                name_str = name.upper() if name else None
            try:
                _ = description.search
                desc_regex = description
                desc_str = None
            except AttributeError:  # search didn't exist
                desc_str = description.upper() if description else None
                desc_regex = None

        project_generator = self.list(status=status)
        matches = []
        for project in project_generator:
            if self._is_project_a_match(project, name_str, name_regex, desc_str, desc_regex, any_):
                matches.append(project)
        return matches

    @staticmethod
    def _is_project_a_match(project, name_str, name_regex, desc_str, desc_regex, any_, **kwargs):
        """
        Given a Project, find out if it is a match for our regular expressions or strings.

        :param project: the Project to check
        :type project: Project
        :param name_str: the uppercased name of the Project to match as a string (case-insensitive) or None
        :type name_str: str
        :param name_regex: a re.compile object to call .search() to see if it matches the Project name or None
        :type name_regex: typing.Pattern
        :param desc_str: an uppercased string that is part of or the entire description (case-insensitive) or None
        :type desc_str: str
        :param desc_regex: a re.compile object to call .search() to see if it matches the Project description or None
        :type desc_regex: typing.Pattern
        :param any_: if truthy, returns a True if name OR description match. Else returns true only if name AND
                    description matched
        :return: True if all non-None parameters matched the Project's name and/or description
        :rtype: bool
        """
        if not any_ and kwargs.get('any'):
            any_ = kwargs.pop('any')
        project_name = project.name if project.name else ""
        project_description = project.description if project.description else ""
        name_str_match = name_str is None or name_str in project_name.upper()
        name_regex_match = name_regex is None or name_regex.search(project_name)
        desc_str_match = desc_str is None or desc_str in project_description.upper()
        desc_regex_match = desc_regex is None or desc_regex.search(project_description)
        name_matched = name_str_match and name_regex_match
        desc_matched = desc_str_match and desc_regex_match
        if any_:
            return name_matched or desc_matched
        else:
            return name_matched and desc_matched

    def get(self, project):
        """
        Get just one Project.

        :param project: a Project object or ID
        :type project: Project|int
        :return: a Project object if found, raises an error if not found
        :rtype: Project
        """
        project = int(project)
        url = self.GET_URL.format(base_url=self.url, project_id=project)
        return self._get(url)

    def list(self, status=None):
        """
        Get a list of Basecamp projects visible to the user.

        :param status: optionally can be 'archived' or 'trashed' to get projects of that type
        :type status: str
        :return: a generator of Project objects
        :rtype: collections.Iterable[Project]
        """
        params = {}
        if status is not None:
            params['status'] = status
        url = self.LIST_URL.format(base_url=self.url)
        return self._get_list(url, params)

    def modify_access(self, project, grant=None, revoke=None):
        """
        Change who is allowed to access a given Project. `grant` and `revoke` take a list of Person objects or a list
        of Person IDs as integers. They can both be specified at the same time.

        :param project: a Project object or ID
        :type project: Project|int
        :param grant: a list of Person objects or Person IDs (ints) to grant access
        :type grant: list[people.Person|int]
        :param revoke: a list of Person objects or Person IDs (ints) to remove from the Project
        :type revoke: list[people.Person|int]
        :return: a response object
        :rtype: requests.Response
        """
        if grant is None and revoke is None:
            raise ValueError("Can't modify access without specifying at least the grant or revoke parameters")
        data = {}
        if grant:
            data['grant'] = util.normalize_acl(grant)
        if revoke:
            data['revoke'] = util.normalize_acl(revoke)
        project = int(project)
        url = self.MODIFY_ACCESS_URL.format(base_url=self.url, project_id=project)
        resp = self._api._session.put(url, json=data)
        return resp

    def trash(self, project):
        """
        Trash the given project. Trashed projects will be deleted from Basecamp 3 after 30 days.
        :param project: a Project object or ID
        """
        project = int(project)
        url = self.TRASH_URL.format(base_url=self.url, project_id=project)
        self._delete(url)

    def update(self, project, name=False, description=False):
        """
        Change the given Project's name and/or description.

        :param project: a Project object or ID
        :type project: Project|int
        :param name: the new name for this Project. A value of False means no change.
        :type name: str
        :param description: the new description for this Project. A value of False means no change.
        :type description: str

        """
        if name is False and description is False:
            raise ValueError("Nothing to update for Project %s" % project)
        project = int(project)
        data = {}
        if name is not False:
            data['name'] = name
        if description is not False:
            data['description'] = description
        url = self.UPDATE_URL.format(base_url=self.url, project_id=project)
        return self._update(url, data=data)

    def _create_from_template(self, name, description, template, timeout=CREATION_FROM_TEMPLATE_TIMEOUT):
        """
        Synchronously creates a Project from a Template, handling the polling of a ProjectConstruction object so that
        the user doesn't have to.

        If a Project is not finished being created before the end of `timeout`, ProjectCreationTimedOutError is raised.

        :param name: the name of the new Project
        :type name: str
        :param description: (optional) the description of the new Project
        :type description: str
        :param template: a Template object or ID
        :type template: basecampy3.endpoints.templates.Template|int
        :param timeout: number of seconds to wait. If not specified, a default timeout defined in the class will be used
        :type timeout: int
        :return: a new Project created from the given Template
        :rtype: Project
        """
        creation_status = self._api.project_constructions.create_project(template=template, name=name,
                                                                         description=description)
        counter = 0
        # usually projects get created pretty fast. Pause for 1 second before checking again.
        while not creation_status.ready:
            time.sleep(1)
            creation_status.refresh()
            counter += 1
            if counter >= timeout:
                msg = u"Project took more than " \
                      u"{seconds} seconds to be created.".format(seconds=timeout)
                ex = ProjectCreationTimedOutError(message=msg)
                raise ex
        return creation_status.project
