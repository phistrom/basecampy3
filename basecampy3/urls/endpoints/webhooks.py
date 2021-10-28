# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs
from .. import util


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
        return self._get("/buckets/{project}/webhooks/{webhook}.json",
                         project=project, webhook=webhook)

    def create(self, project, payload_url, types=None, **kwargs):
        """
        Create a new Webhook in the given Project.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#create-a-webhook

        :param project: the ID of a Project
        :type project: int
        :param payload_url: the URL to send update notifications to
        :type payload_url: typing.AnyStr
        :param types: a list of Types of objects to receive notifications about
                      (by default, get notifications for updates to any
                      supported type)
        :type types: typing.Iterable[typing.AnyStr]|None
        :param kwargs: additional JSON parameters (for future use)
        :type kwargs: typing.Any
        :return: the URL for creating new Webhooks in the given Project
        :rtype: basecampy3.urls.URL
        """

        kwargs["payload_url"] = payload_url
        kwargs["types"] = types

        kwargs = util.filter_unused(kwargs)

        return self._post("/buckets/{project}/webhooks.json", project=project,
                          json_dict=kwargs)

    def update(self, project, webhook, payload_url, types=None, active=None, **kwargs):
        """
        Modify a Webhook.

        https://github.com/basecamp/bc3-api/blob/master/sections/webhooks.md#update-a-webhook

        :param project: the ID of a Project
        :type project: int
        :param webhook: the ID of a Webhook
        :type webhook: int
        :param payload_url: required (provide the old URL if you don't want
                            to change it)
        :type payload_url: typing.AnyStr
        :param types: modify the list of Types this Webhook should notify for
        :type types: typing.Iterable[typing.AnyStr]|None
        :param active: whether this Webhook is enabled and sending
                       notifications or not
        :type active: bool
        :return: the URL for modifying the desired Webhook
        :rtype: basecampy3.urls.URL
        """
        kwargs["payload_url"] = payload_url
        kwargs["types"] = types
        kwargs["active"] = active
        kwargs = util.filter_unused(kwargs)
        return self._put("/buckets/{project}/webhooks/{webhook}.json",
                         project=project, webhook=webhook, json_dict=kwargs)

    def delete(self, project, webhook):
        """
        Delete the given Webhook.

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
