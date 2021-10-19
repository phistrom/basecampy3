# -*- coding: utf-8 -*-
"""
Base class for Recording objects in the Basecamp 3 API.
"""

import abc
import six
from .base import EndpointURLs
from .. import util


@six.add_metaclass(abc.ABCMeta)
class RecordingEndpointURLs(EndpointURLs):
    """
    Not all Recordings support all of these features.
    For instance, Comments do not support Client Visibility.

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

    def trash(self, project, recording):
        """
        Trash a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#trash-a-recording

        :return: the URL for trashing a Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{recording}/status/trashed.json",
                         project=project, recording=recording)

    def archive(self, project, recording):
        """
        Archive a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md#archive-a-recording

        :return: the URL for archiving a Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{recording}/status/archived.json",
                         project=project, recording=recording)

    def unarchive(self, project, recording):
        """
        Unarchive a Recording.

        :return: the URL for unarchiving a Recording.
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{recording}/status/active.json",
                         project=project, recording=recording)

    def client_visibility(self, project, recording, visible_to_clients):
        """
        Modify whether a particular Recording object is visible to the Client.
        Not supported by Comment objects.

        https://github.com/basecamp/bc3-api/blob/master/sections/client_visibility.md#toggle-client-visibility

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :param visible_to_clients: True if a recording should be visible to clients
        :type visible_to_clients: bool
        :return: the URL to use to toggle visibility of the Recording
        :rtype: basecampy3.urls.URL
        """
        json_dict = {
            "visible_to_clients": visible_to_clients,
        }
        return self._put("/buckets/{project}/recordings/{recording}/client_visibility.json",
                         project=project, recording=recording, json_dict=json_dict)

    def events(self, project, recording):
        """
        Get a list of changes made to a given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/events.md#get-events

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL to retrieve the Events on the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/recordings/{recording}/events.json",
                         project=project, recording=recording)

    def list_subscriptions(self, project, recording):
        """
        List the subscribers of a given Recording. Subscribers are People who
        are notified when a Recording is updated.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#get-subscription

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL for getting the list of People subscribed to a Recording
        :rtype:
        """
        return self._get("/buckets/{project}/recordings/{recording}/subscription.json",
                         project=project, recording=recording)

    def subscribe_myself(self, project, recording):
        """
        Subscribe the current user to the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#subscribe-current-user

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL for subscribing the current user to the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/recordings/{recording}/subscription.json",
                          project=project, recording=recording)

    def unsubscribe_myself(self, project, recording):
        """
        Unsubscribe the current user from the given Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#unsubscribe-current-user

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL for unsubscribing the current user from the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._delete("/buckets/{project}/recordings/{recording}/subscription.json",
                            project=project, recording=recording)

    def update_subscriptions(self, project, recording):
        """
        Add/remove subscribers to a Recording.

        https://github.com/basecamp/bc3-api/blob/master/sections/subscriptions.md#update-subscription

        :param project: the ID of a Project
        :type project: int
        :param recording: the ID of a Recording
        :type recording: int
        :return: the URL for modifying the subscriber list of the desired Recording
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/recordings/{recording}/subscription.json",
                         project=project, recording=recording)
