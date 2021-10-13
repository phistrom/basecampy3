# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs


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

    def create(self, project, vault):
        """
        Create a new Upload.

        https://github.com/basecamp/bc3-api/blob/master/sections/uploads.md#create-an-upload

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :return: the URL for creating a new Upload
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/vaults/{vault}/uploads.json",
                          project=project, vault=vault)

    def update(self, project, upload):
        """
        Modify an Upload's base name or description.

        :param project: the ID of a Project
        :type project: int
        :param upload: the ID of an Upload
        :type upload: int
        :return: the URL for modifying an Upload
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/uploads/{upload}.json",
                         project=project, upload=upload)
