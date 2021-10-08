# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class ClientCorrespondences(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/client_correspondences.md
    """

    def list(self, project):
        """
        Get a list of Client Correspondences for a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_correspondences.md#get-client-correspondences

        :param project: the ID of a Project
        :type project: int
        :return: the URL for retrieving a given Client Correspondence
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/client/correspondences.json", project=project)

    def get(self, project, client_correspondence):
        """
        Get a Client Correspondence by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_correspondences.md#get-a-client-correspondence

        :param project: the ID of a Project
        :type project: int
        :param client_correspondence: the ID of a Client Correspondence
        :type client_correspondence: int
        :return: the URL to retrieve the desired Client Correspondence
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/client/correspondences/{client_correspondence}.json",
                         project=project, client_correspondence=client_correspondence)
