# -*- coding: utf-8 -*-
"""
URLs related to Question Answer objects in the Basecamp 3 API.
"""

from .recordings import RecordingEndpointURLs


class QuestionAnswers(RecordingEndpointURLs):
    """
    Almost none of the Recording endpoint URLs work for Question Answers:
      * Archiving/Unarchiving Answers is unsupported.
      * Client Visibility is unsupported.
      * Events are unsupported.
      * Subscriptions are unsupported.
      * Trashing is unsupported.

    https://github.com/basecamp/bc3-api/blob/master/sections/question_answers.md
    https://3.basecamp-help.com/article/50-automatic-check-ins
    """

    RECORD_TYPE = "Question::Answer"

    def list_by_question(self, project, question):
        """
        Get a list of Question Answers for the given Question.

        https://github.com/basecamp/bc3-api/blob/master/sections/question_answers.md#get-question-answers

        :param project: the ID of a Project
        :type project: int
        :param question: the ID of a Question
        :type question: int
        :return: the URL for retrieving the list of Question Answers for the desired Question
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/questions/{question}/answers.json",
                         project=project, question=question)

    def get(self, project, answer):
        """
        Get a Question Answer by ID.

        https://github.com/basecamp/bc3-api/blob/master/sections/question_answers.md#get-a-question-answer

        :param project: the ID of a Project
        :type project: int
        :param answer: the ID of a Question Answer
        :type answer: int
        :return: the URL to get the desired Question Answer
        :rtype: basecampy3.urls.URL
        """
        return self._get("/buckets/{project}/question_answers/{answer}.json",
                         project=project, answer=answer)
