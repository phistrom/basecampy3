# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Schedules(EndpointURLs):
    def get(self, project, schedule):
        """
        Get a Schedule by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/schedules.md#get-schedule

        :param project: the ID of a Project
        :type project: int
        :param schedule: the ID of a Schedule
        :type schedule: int
        :return: the URl for retrieving the desired Schedule
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/schedules/{schedule}.json",
                         proejct=project, schedule=schedule)
