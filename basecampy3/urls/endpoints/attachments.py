# -*- coding: utf-8 -*-
"""
URLs related to Attachment objects in the Basecamp 3 API.
"""
import mimetypes
import os

from .base import EndpointURLs


class Attachments(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md
    """

    def create(self, filepath, name=None, content_type=None, **kwargs):
        """
        Create a new attachment (upload).

        https://github.com/basecamp/bc3-api/blob/master/sections/attachments.md#create-an-attachment

        :param filepath: path to the file to upload to Basecamp
        :type filepath: typing.AnyStr
        :param name: the name of the file to upload
        :type name: typing.AnyStr|None
        :param content_type: the MIME type of the file. Will try to auto-detect
                             from file extension if not provided.
        :type content_type: typing.AnyStr|None
        :param kwargs: additional parameters for `requests`
        :type kwargs: typing.AnyStr
        :return: a URL to upload a file to
        :rtype: basecampy3.urls.URL
        """
        if not name:
            name = os.path.basename(filepath)
        if not content_type:
            content_type, _ = mimetypes.guess_type(name)

        params = {
            "name": name,
        }
        params.update(kwargs)

        headers = {
            "Content-Type": content_type,
        }

        return self._post("/attachments.json", params=params,
                          headers=headers, filepath=filepath)
