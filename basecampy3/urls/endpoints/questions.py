# -*- coding: utf-8 -*-
"""
"""

from .base import EndpointURLs


class Questions(EndpointURLs):
    def list(self, project, questionnaire):
        """
        Get a list of Questions for the given Questionnaire.

        https://github.com/basecamp/bc3-api/blob/master/sections/questions.md#get-questions

        :param project: the ID of a Project
        :type project: int
        :param questionnaire: the ID of a Questionnaire
        :type questionnaire: int
        :return: the URL for retrieving the Questions from the desired Questionnaire
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/questionnaires/{questionnaire}/questions.json",
                         project=project, questionnaire=questionnaire)

    def get(self, project, question):
        """
        Get a Question by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/questions.md#get-a-question

        :param project: the ID of a Project
        :type project: int
        :param question: the ID of a Question
        :type question: int
        :return: the URL for retrieving the desired Question
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/questions/{question}.json",
                         project=project, question=question)
