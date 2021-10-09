# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Templates(EndpointURLs):
    """
    Project Blueprints or Templates.

    https://github.com/basecamp/bc3-api/blob/master/sections/templates.md
    https://3.basecamp-help.com/article/66-templates
    """
    def list(self, status=None, **kwargs):
        """
        List all active templates visible to the current user.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#get-templates

        :param status: active, archived, or trashed to filter by that state
        :type status: str|None
        :param kwargs: additional query string parameters (not currently used)
        :type kwargs: str
        :return: the URL for listing Templates
        :rtype: basecampy3.urls.URL
        """
        params = {
            "status": status
        }
        params.update(kwargs)
        return self._get("/templates.json", params=params)

    def get(self, template):
        """
        Get Template by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#get-a-template

        :param template: the ID of a Template
        :type template: int
        :return: the URL for retrieving the desired Template
        :rtype: basecampy3.urls.URL
        """
        return self._get("/templates/{template}.json", template=template)

    def create(self):
        """
        Create a new Template.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#create-a-template

        :return: the URL for creating a Template
        :rtype: basecampy3.urls.URL
        """
        return self._post("/templates.json")

    def update(self, template):
        """
        Modify an existing Template's name and/or description.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#update-a-template

        :param template: the ID of a Template
        :type template: int
        :return: the URL for modifying the desired Template
        :rtype: basecampy3.urls.URL
        """
        return self._put("/templates/{template}.json", template=template)

    def trash(self, template):
        """
        Trash a Template.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#trash-a-template

        :param template: the ID of a template
        :type template: int
        :return: the URL for trashing the desired Template
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/templates/{template}.json", template=template)



