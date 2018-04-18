from ._base import BasecampEndpoint, BasecampObject
from . import projects, templates


class ProjectConstruction(BasecampObject):
    @property
    def project(self):
        """
        When the status of a Project Construction is "completed", we also get the Project data in the JSON response.
        This allows us to construct a Project object without another hit to the API.

        :return: None if the Project isn't ready yet or a Project object if it is
        :rtype: projects.Project
        """
        if 'project' not in self._values:
            return None
        return projects.Project(json_dict=self._values['project'], endpoint=self._endpoint._api.projects)

    @property
    def ready(self):
        """
        A shortcut for self.status == "completed". This variable does not change between invocations of refresh().

        :return: True if and only if this Project Construction's status is "completed"
        :rtype: bool
        """
        return self.status == "completed"

    def __int__(self):
        return int(self.id)


class ProjectConstructions(BasecampEndpoint):
    OBJECT_CLASS = ProjectConstruction

    PROJECT_CREATION_STATUS_URL = "{base_url}/templates/{template_id}/project_constructions/{project_construction_id}.json"
    CREATE_FROM_TEMPLATE_URL = "{base_url}/templates/{template_id}/project_constructions.json"

    def create_project(self, template, name, description=""):
        """
        Creates a new project from the given template. Requires a name and optionally a description.
        Beware that this function does not return a Project object. When made from a template, Projects are made
        asynchronously. This function returns a new `ProjectConstruction` object which allows you to check on the
        status of a project being built from your template.

        :param template: a Template object or ID
        :type template: templates.Template|int
        :param name: a name for this new Project
        :type name: str
        :param description: (optional) a description for this new Project
        :type description: str
        :return: a ProjectConstruction object that can be polled for if the Project is finished being
                 created yet
        :rtype: ProjectConstruction
        """

        template = int(template)

        data = {
            'project': {
                'name': name,
                'description': description,
            }
        }
        url = self.CREATE_FROM_TEMPLATE_URL.format(base_url=self.url, template_id=template)
        project_creation_status = self._create(url, data=data)
        return project_creation_status

    def get(self, template, construction):
        """
        Gets a ProjectConstruction by its ID and the ID of the Template it was created from. This object represents
        whether the Project is finished being created or not.

        :param template: a Template object or ID
        :type template: templates.Template|int
        :param construction: a ProjectConstruction object or ID
        :type construction: ProjectConstruction|int
        :return: a ProjectConstruction object.
        :rtype: ProjectConstruction
        """
        template = int(template)
        construction = int(construction)
        url = self.PROJECT_CREATION_STATUS_URL.format(base_url=self.url, template_id=template,
                                                      project_construction_id=construction)
        return self._get(url)
