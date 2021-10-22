# -*- coding: utf-8 -*-
"""
URLs related to Project objects in the Basecamp 3 API.
"""

from .base import EndpointURLs
from .. import util


class Projects(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/projects.md
    https://3.basecamp-help.com/article/25-teams-and-project#projects
    """

    def list(self, status=None, **kwargs):
        """
        Get a list of projects. Unless you specify "archived" or "trashed" as
        the status, the default is to show "active" projects. However, you may
        _not_ specify "active" as a status.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#get-all-projects

        :param status: archived, or trashed
        :type status: str|None
        :return: a URL that will list the desired projects
        :rtype: basecampy3.urls.URL
        """
        params = {
            "status": status,
        }
        params.update(kwargs)

        return self._get("/projects.json", params=params)

    def get(self, project):
        """
        Get a project by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#get-a-project

        :param project: the ID of a Project
        :type project: int
        :return: a URL to get the details of a Project
        :rtype: basecampy3.urls.URL
        """
        return self._get("/projects/{project}.json", project=project)

    def create(self, name, description=None, **kwargs):
        """
        Create a new project.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#create-a-project

        :param name: the name of this new Project
        :type name: typing.AnyStr
        :param description: optional description of the new Project
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (unused at this time)
        :type kwargs: typing.AnyStr
        :return: the URL to create a new Project item
        :rtype: basecampy3.urls.URL
        """
        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._post("/projects.json", json_dict=kwargs)

    def update(self, project, name=None, description=None, **kwargs):
        """
        Rename a project or change its description.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#update-a-project

        :param project: the ID of a Project
        :type project: int
        :param name: a new name for this Project
        :type name: typing.AnyStr|None
        :param description: a new description for this Project
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (unused at this time)
        :type kwargs: typing.AnyStr|None
        :return: a URL to update a Project
        :rtype: basecampy3.urls.URL
        """

        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._put("/projects/{project}.json", project=project,
                         json_dict=kwargs)

    def trash(self, project):
        """
        Trash a project.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#trash-a-project

        :param project: the ID of a Project
        :type project: int
        :return: a URL to trash a Project
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/projects/{project}.json", project=project)

    def update_membership(self, project, grant=None, revoke=None, create=None, **kwargs):
        """
        Modify who can access a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#update-who-can-access-a-project

        :param project: the ID of a Project
        :type project: int
        :return: the URL to modify who has access to a Project
        :rtype: basecampy3.urls.URL
        """
        kwargs["grant"] = grant
        kwargs["revoke"] = revoke
        kwargs["create"] = create

        for key in ("grant", "revoke", "create"):
            access_list = kwargs[key]
            if access_list:
                # convert any BasecampObjects to just their `id`
                kwargs[key] = {k: getattr(v, "id", v) for k, v in access_list.items()}
        kwargs = util.filter_unused(kwargs)
        return self._put("/projects/{project}/people/users.json",
                         project=project, json_dict=kwargs)

    def create_from_template(self, template, name, description=None, **kwargs):
        """
        Create a Project from a Template.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#create-a-project-construction

        :param template: the ID of a Template
        :type template: int
        :param name: the name for this new Project
        :type name: typing.AnyStr
        :param description: an optional description for this new Project
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (not currently used)
        :type kwargs: typing.Any
        :return: the URL for creating a Project from the desired Template
        :rtype: basecampy3.urls.URL
        """

        kwargs["name"] = name
        kwargs["description"] = description
        kwargs = util.filter_unused(kwargs)

        json_dict = {
            "project": kwargs,
        }

        return self._post("/templates/{template}/project_constructions.json",
                          template=template, json_dict=json_dict)

    def get_construction_status(self, template, project_construction):
        """
        Projects created from a Template are created asynchronously. Use this
        endpoint to see if a Project has finished being created.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#get-a-project-construction

        :param template: the ID of a Template
        :type template: int
        :param project_construction: the ID of a Project Construction
        :type project_construction: int
        :return: the URL for checking the desired Project Construction's status
        :rtype: basecampy3.urls.URL
        """
        return self._get("/templates/{template}/project_constructions/{project_construction}.json",
                         template=template, project_construction=project_construction)
