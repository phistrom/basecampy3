# -*- coding: utf-8 -*-
"""
URLs related to Schedule Entry objects in the Basecamp 3 API.
"""

from datetime import datetime

from .recordings import RecordingEndpointURLs
from .. import util

_omit = object()
"""
Used instead of `None` as default values in the `update()` function since 
`None` may be a value the user **wants** to change an attribute to.
"""


class ScheduleEntries(RecordingEndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md
    https://3.basecamp-help.com/article/49-schedule
    """
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

    def create(self, project, schedule, summary, starts_at, ends_at, description=None,
               participant_ids=None, all_day=None, notify=None, **kwargs):
        """
        Create Schedule Entry in the given Schedule.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#create-a-schedule-entry

        :param int project: the ID of a Project
        :param int schedule: the ID of a Schedule
        :param str summary: what this schedule entry is about
        :param datetime starts_at: when this schedule entry begins
        :param datetime ends_at: when this schedule entry ends
        :param str description: rich text (HTML) information about the new entry
        :param participant_ids: an array of People that will participate in this entry
        :type participant_ids: int[]|basecampy3.endpoints.people.Person[]
        :param bool all_day: if True, entry will be all day(s) denoted by
                             start_at and ends_at
        :param bool notify: if True, participants will be notified about the entry
        :param kwargs: additional JSON parameters (not currently used)
        :return: the URL for creating a new Schedule Entry in the desired Schedule
        :rtype: basecampy3.urls.URL
        """
        kwargs["summary"] = summary
        starts_at = util.fix_naive_datetime(starts_at).replace(microsecond=0)
        ends_at = util.fix_naive_datetime(ends_at).replace(microsecond=0)

        kwargs["starts_at"] = starts_at.isoformat()
        kwargs["ends_at"] = ends_at.isoformat()
        kwargs["description"] = description
        kwargs["participant_ids"] = participant_ids
        kwargs["all_day"] = bool(all_day)
        kwargs["notify"] = bool(notify)

        kwargs = util.filter_unused(kwargs)

        return self._post("/buckets/{project}/schedules/{schedule}/entries.json",
                          project=project, schedule=schedule, json_dict=kwargs)

    def update(self, project, entry, summary=_omit, starts_at=_omit, ends_at=_omit, description=_omit,
               participant_ids=_omit, all_day=_omit, notify=_omit, **kwargs):
        """
        Modify a Schedule Entry by its ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedule_entries.md#update-a-schedule-entry

        :param project: the ID of a Project
        :type project: int
        :param entry: the ID of a Schedule Entry
        :type entry: int
        :param str summary: what this schedule entry is about
        :param datetime starts_at: when this schedule entry begins
        :param datetime ends_at: when this schedule entry ends
        :param str description: rich text (HTML) information about the new entry
        :param participant_ids: an array of People that will participate in this entry
        :type participant_ids: int[]|basecampy3.endpoints.people.Person[]
        :param bool all_day: if True, entry will be all day(s) denoted by
                             start_at and ends_at
        :param bool notify: if True, participants will be notified about the entry
        :param kwargs: additional JSON parameters (not currently used)
        :return: the URL for modifying the desired Schedule Entry
        :rtype: basecampy3.urls.URL
        """
        # To anyone reading this code going "wtf? Why not just use kwargs?"
        # I wanted the function declaration to be explicit to help
        # with auto-complete and documentation. From what I can tell, PyCharm
        # will complain about, and not use, parameters that are in the kwargs
        # dictionary, even when your code clearly tries to access those keys
        # in the kwargs dictionary. So here is `args` which is basically
        # reinventing the wheel.

        args = {
            "summary": summary,
            "starts_at": starts_at,
            "ends_at": ends_at,
            "description": description,
            "participant_ids": participant_ids,
            "all_day": all_day,
            "notify": notify,
        }

        # filter out parameters the user did not provide
        args = {k: v for k, v in args.items() if v is not _omit}

        # convert starts_at or ends_at, if provided, to timezone-aware datetime
        for dtname in ("starts_at", "ends_at"):
            if dtname in args:
                dt = args[dtname]
                dt = util.fix_naive_datetime(dt)
                args[dtname] = dt.replace(microsecond=0).isoformat()

        # ensure bool params, if provided, are actual booleans
        for boolname in ("all_day", "notify"):
            if boolname in args:
                args[boolname] = bool(args[boolname])
        kwargs.update(args)
        return self._put("/buckets/{project}/schedule_entries/{entry}.json",
                         project=project, entry=entry, json_dict=kwargs)
