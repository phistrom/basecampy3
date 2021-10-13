# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class TodoSets(EndpointURLs):
    def get(self, project, todo_set):
        return self._get("/buckets/{project}/todosets/{todo_set}.json",
                         project=project, todo_set=todo_set)
