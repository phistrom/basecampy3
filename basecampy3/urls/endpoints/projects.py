# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Projects(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/projects.md
    """

    def list(self, status=None, **kwargs):
        """
        Get a list of projects.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#get-all-projects

        :param status: active, archived, or trashed
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

    def create(self):
        """
        Create a new project.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#create-a-project

        :return: the URL to create a new Project item
        :rtype: basecampy3.urls.URL
        """
        return self._post("/projects.json")

    def update(self, project):
        """
        Rename a project or change its description.

        https://github.com/basecamp/bc3-api/blob/master/sections/projects.md#update-a-project

        :param project: the ID of a Project
        :type project: int
        :return: a URL to update a Project
        :rtype: basecampy3.urls.URL
        """
        return self._put("/projects/{project}.json", project=project)

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

    def update_membership(self, project):
        """
        Modify who can access a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/people.md#update-who-can-access-a-project

        :param project: the ID of a Project
        :type project: int
        :return: the URL to modify who has access to a Project
        :rtype: basecampy3.urls.URL
        """
        return self._put("/projects/{project}/people/users.json", project=project)

    def create_from_template(self, template):
        """
        Create a Project from a Template.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#create-a-project-construction

        :param template: the ID of a Template
        :type template: int
        :return: the URL for creating a Project from the desired Template
        :rtype: basecampy3.urls.URL
        """
        return self._post("/templates/{template}/project_constructions.json", template=template)

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
