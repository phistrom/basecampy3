# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class ClientApprovals(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/client_approvals.md
    """

    def list(self, project):
        """
        Get a list of all Client Approvals for a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_approvals.md#get-client-approvals

        :param project: the ID of a Project
        :type project: int
        :return: a URL for retrieving a list of Client Approvals for the desired Project
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/client/approvals.json", project=project)

    def get(self, project, client_approval):
        """
        Get a Client Approval by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_approvals.md#get-a-client-approval

        :param project: the ID of a Project
        :type project: int
        :param client_approval: the ID of a Client Approval
        :type client_approval: int
        :return: the URL for retrieving details about the desired Client Approval
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/client/approvals/{client_approval}.json",
                         project=project, client_approval=client_approval)
