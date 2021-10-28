# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs
from .. import util


class Vaults(RecordingEndpointURLs):
    """
    Folders.
    https://github.com/basecamp/bc3-api/blob/master/sections/vaults.md
    """

    RECORD_TYPE = "Vault"

    def list_vault_by_vault(self, project, vault):
        """
        Get Vaults by their parent Vault.

        https://github.com/basecamp/bc3-api/blob/master/sections/vaults.md#get-vaults

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :return: the URL for retrieving a list of Vaults for the desired parent Vault
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/vaults/{vault}/vaults.json",
                         project=project, vault=vault)

    def get(self, project, vault):
        """
        Get a Vault by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/vaults.md#get-a-vault

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :return: the URL for retrieving the desired Vault
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/vaults/{vault}.json",
                         project=project, vault=vault)

    def create(self, project, vault, title, **kwargs):
        """
        Create a new Vault in the given parent Vault.

        https://github.com/basecamp/bc3-api/blob/master/sections/vaults.md#create-a-vault

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault to be the new Vault's parent
        :type vault: int
        :param title: the name for this vault
        :type title: typing.AnyStr
        :param kwargs: additional JSON parameters (for future use)
        :type kwargs: typing.Any
        :return: the URL for creating new Vaults within the desired Vault
        :rtype: basecampy3.urls.URL
        """
        kwargs["title"] = title
        kwargs = util.filter_unused(kwargs)
        return self._post("/buckets/{project}/vaults/{vault}/vaults.json",
                          project=project, vault=vault, json_dict=kwargs)

    def update(self, project, vault, title, **kwargs):
        """
        Update a Vault's title.

        https://github.com/basecamp/bc3-api/blob/master/sections/vaults.md#update-a-vault

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault to modify
        :type vault: int
        :param title: a new name for this Vault
        :type title: typing.AnyStr
        :param kwargs: additional JSON parameters
        :type kwargs: typing.Any
        :return: the URL for modifying the desired Vault
        :rtype: basecampy3.urls.URL
        """

        kwargs["title"] = title
        kwargs = util.filter_unused(kwargs)

        return self._put("/buckets/{project}/vaults/{vault}.json",
                         project=project, vault=vault, json_dict=kwargs)
