from . import _base
import six


@six.python_2_unicode_compatible
class Answer(_base.BasecampObject):
    """
    A question answer on Basecamp 3
    """

    def __str__(self):
        try:
            return u"Answer {} - by {}".format(self.id, self.creator.get('name'))
        except:
            return super(Answer, self).__str__()


class Answers(_base.BasecampEndpoint):
    OBJECT_CLASS = Answer

    LIST_ANSWERS_URL = "{base_url}/buckets/{project_id}/questions/{question_id}/answers.json"

    def list(self, project, question):
        """
        Get a list of answers in question

        :param project: a project containing question
        :type project: basecampy3.endpoints.projects.Project|int
        :param question: id of question to list answers from
        :type question: int
        :return: a list of Answer objects
        :rtype: collections.Iterable[Answer]
        """
        assert project is not None
        assert question is not None

        project = int(project)
        url = self.LIST_ANSWERS_URL.format(base_url=self.url, project_id=project, question_id=question)

        return self._get_list(url)
