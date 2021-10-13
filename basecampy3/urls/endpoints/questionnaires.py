# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Questionnaires(EndpointURLs):
    """
    https://github.com/basecamp/bc3-api/blob/master/sections/questionnaires.md
    """
    def get(self, project, questionnaire):
        """
        Get a Questionnaire by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/questionnaires.md#get-questionnaire

        :param project: the ID of a Project
        :type project: int
        :param questionnaire: the ID of a Questionnaire
        :type questionnaire: int
        :return: the URL for getting the desired Questionnaire
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/questionnaires/{questionnaire}/questions.json",
                         project=project, questionnaire=questionnaire)
