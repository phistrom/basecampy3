# -*- coding: utf-8 -*-
"""
URLs related to Project Template objects in the Basecamp 3 API.
"""

from .base import EndpointURLs
from .. import util


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

        :param status: archived, or trashed to filter by that state
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

    def create(self, name, description=None, **kwargs):
        """
        Create a new Template.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#create-a-template

        :param name: the name for this Template
        :type name: typing.AnyStr
        :param description: an optional description for this Template
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON params (not currently used)
        :type kwargs: typing.Any
        :return: the URL for creating a Template
        :rtype: basecampy3.urls.URL
        """
        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._post("/templates.json", json_dict=kwargs)

    def update(self, template, name=None, description=None, **kwargs):
        """
        Modify an existing Template's name and/or description.

        https://github.com/basecamp/bc3-api/blob/master/sections/templates.md#update-a-template

        :param template: the ID of a Template
        :type template: int
        :param name: a new name for this Template
        :type name: typing.AnyStr|None
        :param description: a new description for this Template
        :type description: typing.AnyStr|None
        :param kwargs: additional JSON parameters (not currently used)
        :type kwargs: typing.Any
        :return: the URL for modifying the desired Template
        :rtype: basecampy3.urls.URL
        """
        kwargs["name"] = name
        kwargs["description"] = description

        kwargs = util.filter_unused(kwargs)

        return self._put("/templates/{template}.json", template=template, json_dict=kwargs)

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



