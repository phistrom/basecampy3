# -*- coding: utf-8 -*-
"""
"""

import abc
import six
from .base import EndpointURLs
from .. import util


@six.add_metaclass(abc.ABCMeta)
class RecordingEndpointURLs(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md
    """

    RECORD_TYPE = None
    """The string to pass in to the ?type={type} query string. This should be overriden by inheriting classes."""

    def list(self, project=None, status="active", sort="created_at", direction="desc", **kwargs):
        """
        Get a paginated list of records.

        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#get-recordings

        :param project: the ID of a project
        :type project: int|None
        :param status: active, archived, or trashed
        :type status: str|None
        :param sort: created_at or updated_at
        :type sort: str|None
        :param direction: the sort direction "desc" or "asc"
        :type direction: str|None
        :param kwargs: additional query string parameters
        :type kwargs: str
        :return: a URL to get the list of requested Recordings
        :rtype: basecampy3.urls.URL
        """
        rectype = self.RECORD_TYPE
        params = {
            "type": rectype,
            "project": project,
            "status": status,
            "sort": sort,
            "direction": direction,
        }
        params.update(kwargs)
        params = util.filter_unused(params)
        return self._get("/projects/recordings.json", params=params)

    def trash(self):
        """
        Trash a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#trash-a-recording

        :return: the URL for trashing a Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project_id}/recordings/{record_id}/status/trashed.json")

    def archive(self):
        """
        Archive a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#archive-a-recording

        :return: the URL for archiving a Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project_id}/recordings/{record_id}/status/archived.json")

    def unarchive(self):
        """
        Unarchive a Recording.

        :return: the URL for unarchiving a Recording.
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project_id}/recordings/{record_id}/status/active.json")

    def client_visibility(self, project, record):
        """
        Modify whether a particular Recording object is visible to the Client.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_visibility.md#toggle-client-visibility

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL to use to toggle visibility of the Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{record}/client_visibility.json",
                         project=project, record=record)

    def events(self, project, record):
        """
        Get a list of changes made to a given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/events.md#get-events

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL to retrieve the Events on the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/recordings/{record}/events.json",
                         project=project, record=record)

    def list_subscriptions(self, project, record):
        """
        List the subscribers of a given Recording. Subscribers are People who
        are notified when a Recording is updated.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#get-subscription

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL for getting the list of People subscribed to a Recording
        :rtype:
        """
        return self._get("/buckets/{project}/recordings/{record}/subscription.json",
                         project=project, record=record)

    def subscribe_myself(self, project, record):
        """
        Subscribe the current user to the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#subscribe-current-user

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL for subscribing the current user to the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/recordings/{record}/subscription.json",
                          project=project, record=record)

    def unsubscribe_myself(self, project, record):
        """
        Unsubscribe the current user from the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#unsubscribe-current-user

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL for unsubscribing the current user from the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/buckets/{project}/recordings/{record}/subscription.json",
                            project=project, record=record)

    def update_subscriptions(self, project, record):
        """
        Add/remove subscribers to a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#update-subscription

        :param project: the ID of a Project
        :type project: int
        :param record: the ID of a Recording
        :type record: int
        :return: the URL for modifying the subscriber list of the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{record}/subscription.json",
                         project=project, record=record)
