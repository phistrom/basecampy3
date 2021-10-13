# -*- coding: utf-8 -*-
"""
"""

from .recordings import RecordingEndpointURLs


class ScheduleEntries(RecordingEndpointURLs):
    RECORD_TYPE = "Schedule::Entry"

    def list_by_schedule(self, project, schedule):
        """
        List the Schedule Entries in the given Schedule.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#get-schedule-entries

        :param project: the ID of a Project
        :type project: int
        :param schedule: the ID of the Schedule
        :type schedule: int
        :return: the URL to retrieve Schedule Entries from the desired Schedule
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/schedules/{schedule}/entries.json",
                         project=project, schedule=schedule)

    def get(self, project, entry):
        """
        Get a Schedule Entry by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#get-a-schedule-entry

        :param project: the ID of a Project
        :type project: int
        :param entry: the ID of a Schedule Entry
        :type entry: int
        :return: the URL for retrieving the desired Schedule Entry
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/schedule_entries/{entry}.json",
                         project=project, entry=entry)

    def create(self, project, schedule):
        """
        Create Schedule Entry in the given Schedule.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#create-a-schedule-entry

        :param project: the ID of a Project
        :type project: int
        :param schedule: the ID of a Schedule
        :type schedule: int
        :return: the URL for creating a new Schedule Entry in the desired Schedule
        :rtype: basecampy3.urls.URL
        """
        return self._post("/buckets/{project}/schedules/{schedule}/entries.json",
                          project=project, schedule=schedule)

    def update(self, project, entry):
        """
        Modify a Schedule Entry by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#update-a-schedule-entry

        :param project: the ID of a Project
        :type project: int
        :param entry: the ID of a Schedule Entry
        :type entry: int
        :return: the URL for modifying the desired Schedule Entry
        :rtype: basecampy3.urls.URL
        """
        return self._put("/buckets/{project}/schedule_entries/{entry}.json",
                         project=project, entry=entry)

