# -*- coding: utf-8 -*-
"""
URLs related to Document objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs
from .. import util


class Documents(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/documents.md
    """

    RECORD_TYPE = "Document"

    def list_by_vault(self, project, vault):
        """
        Get a list of Documents in a given Vault.

        https://github.com/basecamp/bc3-api/blob/master/sections/documents.md#get-documents

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :return: the URL to retrieve a list of Documents in the desired Vault
        :rtype: basecampy3.urls.URL
        """

        return self._get("/buckets/{project}/vaults/{vault}/documents.json",
                         project=project, vault=vault)

    def get(self, project, document):
        """
        Get a Document by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/documents.md#get-a-document

        :param project: the ID of a Project
        :type project: int
        :param document: the ID of a Document
        :type document: int
        :return: the URL to get the desired Document
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/documents/{document}.json",
                         project=project, document=document)

    def create(self, project, vault, title, content, status=None):
        """
        Create a new Document in the given Vault.

        https://github.com/basecamp/bc3-api/blob/master/sections/documents.md#create-a-document

        :param project: the ID of a Project
        :type project: int
        :param vault: the ID of a Vault
        :type vault: int
        :param title: the title of this new Document
        :type title: typing.AnyStr
        :param content: rich text (HTML) content of this Document
        :type content: typing.AnyStr
        :param status: "drafted" by default. Set to "active" to publish immediately.
        :type status: typing.AnyStr
        :return: the URL to create a new Document in the desired Vault
        :rtype: basecampy3.urls.URL
        """
        json_dict = {
            "title": title,
            "content": content,
            "status": status,
        }
        json_dict = util.filter_unused(json_dict)

        return self._post("/buckets/{project}/vaults/{vault}/documents.json",
                          project=project, vault=vault, json_dict=json_dict)

    def update(self, project, document, title=None, content=None):
        """
        Change the title or content of a given Document.

        :param project: the ID of a Project
        :type project: int
        :param document: the ID of a Document
        :type document: int
        :param title: a new title for this Document
        :type title: typing.AnyStr
        :param content: new rich text (HTML) content for this Document
        :type content: typing.AnyStr
        :return: the URL to use to modify the desired Document
        :rtype: basecampy3.urls.URL
        """

        json_dict = {
            "title": title,
            "content": content,
        }
        json_dict = util.filter_unused(json_dict)
        return self._put("/buckets/{project}/documents/{document}.json",
                         project=project, document=document, json_dict=json_dict)
