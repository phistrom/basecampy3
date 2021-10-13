# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Webhooks(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md

    https://3.basecamp-help.com/article/160-chatbots-and-webhooks
    """
    def list(self, project):
        """
        List the Webhooks in a given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#get-webhooks

        :param project: the ID of a Project
        :type project: int
        :return: the URL for listing Webhooks in a desired Project
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/webhooks.json", project=project)

    def get(self, project, webhook):
        """
        Retrieve a Webhook by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#get-a-webhook

        :param project: the ID of a Project
        :type project: int
        :param webhook: the ID of a Webhook
        :type webhook: int
        :return: the URL for retrieving the desired Webhook
        :rtype: basecampy3.urls.URL
        """

    def create(self, project):
        """
        Create a new Webhook in the given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#create-a-webhook

        :param project: the ID of a Project
        :type project: int
        :return: the URL for creating new Webhooks in the given Project
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/webhooks.json", project=project)

    def update(self, project, webhook):
        """
        Modify a Webhook.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#update-a-webhook

        :param project: the ID of a Project
        :type project: int
        :param webhook: the ID of a Webhook
        :type webhook: int
        :return: the URL for modifying the desired Webhook
        :rtype: basecampy3.urls.URL
        """

        return self._put("/buckets/{project}/webhooks/{webhook}.json",
                         project=project, webhook=webhook)

    def delete(self, project, webhook):
        """
        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#destroy-a-webhook
        :param project: the ID of a Project
        :type project: int
        :param webhook: the ID of a Webhook
        :type webhook: int
        :return: the URL for deleting the desired Webhook
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/buckets/{project}/webhooks/{webhook}.json",
                            project=project, webhook=webhook)
