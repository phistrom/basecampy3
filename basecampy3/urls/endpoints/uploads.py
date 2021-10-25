# -*- coding: utf-8 -*-
"""
URLs related to Upload objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs
from .. import util


class Uploads(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md
    """

    RECORD_TYPE = "Upload"

    def list_by_vault(self, project, vault):
        """
        Get a list of Uploads in a given Vault.

        https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md#get-uploads

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :return: the URL for listing Uploads in the desired Vault
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/vaults/{vault}/uploads.json",
                         project=project, vault=vault)

    def get(self, project, upload):
        """
        Get an Upload by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md#get-an-upload

        :param project: the ID of a Project
        :type project: int
        :param upload: the ID of an Upload
        :type upload: int
        :return: the URL for retrieving the desired Upload
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/uploads/{upload}.json",
                         project=project, upload=upload)

    def create(self, project, vault, attachable_sgid, **kwargs):
        """
        Create a new Upload.

        https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md#create-an-upload

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :param attachable_sgid: generated from the create attachment URL
        :type attachable_sgid: typing.AnyStr
        :return: the URL for creating a new Upload
        :rtype: basecampy3.urls.URL
        """
        kwargs["attachable_sgid"] = attachable_sgid

        return self._post("/buckets/{project}/vaults/{vault}/uploads.json",
                          project=project, vault=vault, json_dict=kwargs)

    def update(self, project, upload, base_name=None, description=None):
        """
        Modify an Upload's base name or description.

        https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md#update-an-upload

        :param project: the ID of a Project
        :type project: int
        :param upload: the ID of an Upload
        :type upload: int
        :param base_name: a new name for this file (base name is file name
                          without the extension)
        :type base_name: typing.AnyStr|None
        :param description: a new rich text (HTML) description for this
                            uploaded file
        :type description: typing.AnyStr|None
        :return: the URL for modifying an Upload
        :rtype: basecampy3.urls.URL
        """
        json_dict = {
            "base_name": base_name,
            "description": description,
        }
        json_dict = util.filter_unused(json_dict)
        return self._put("/buckets/{project}/uploads/{upload}.json",
                         project=project, upload=upload, json_dict=json_dict)
