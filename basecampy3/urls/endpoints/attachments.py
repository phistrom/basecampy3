# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Attachments(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md
    """

    def create(self, name, **kwargs):
        """
        Create a new attachment (upload).

        https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md#create-an-attachment

        :param name: the name of the file to upload
        :type name: str
        :param kwargs: additional query string parameters (if any are added in the future)
        :type kwargs: str
        :return: a URL to upload a file to
        :rtype: basecampy3.urls.URL
        """
        params = {
            "name": name,
        }
        params.update(kwargs)

        return self._make_url("POST", "/attachments.json", params=params)
