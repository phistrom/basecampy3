from . import _base
import six


@six.python_2_unicode_compatible
class Person(_base.BasecampObject):
    """
    A user profile on Basecamp 3
    """

    def __str__(self):
        try:
            return u"Person {0.id}: '{0.name}'".format(self)
        except:
            return super(Person, self).__str__()


class People(_base.BasecampEndpoint):
    OBJECT_CLASS = Person

    LIST_PEOPLE_URL = "{base_url}/people.json"
    LIST_BY_PROJECT_URL = "{base_url}/projects/{project_id}/people.json"
    LIST_PINGABLE_URL = "{base_url}/circles/people.json"
    GET_PERSON_URL = "{base_url}/people/{person_id}.json"
    GET_MYSELF_URL = "{base_url}/my/profile.json"

    def list(self, project=None):
        """
        Get a list of people visible to the user.

        :param project: optionally can pick a project to list the people who are members of it
        :type project: basecampy3.endpoints.projects.Project|int
        :return: a list of Person objects
        :rtype: collections.Iterable[Person]
        """
        if project is not None:
            project = int(project)
        if project is not None:
            url = self.LIST_BY_PROJECT_URL.format(base_url=self.url, project_id=project)
        else:
            url = self.LIST_PEOPLE_URL.format(base_url=self.url)
        return self._get_list(url)

    def list_pingable(self):
        """
        Get a list of people that the user can ping
        :return: a list of Person objects
        :rtype: collections.Iterable[Person]
        """
        url = self.LIST_PINGABLE_URL.format(base_url=self.url)
        return self._get_list(url)

    def get(self, oid=None):
        """
        Get Person by ID. If no ID is given, returns the current user's Person
        :param oid: the person's ID
        :type oid: Person|int
        :return: a Person object
        :rtype: Person
        """
        if oid is None:
            url = self.GET_MYSELF_URL.format(base_url=self.url)
        else:
            oid = int(oid)
            url = self.GET_PERSON_URL.format(base_url=self.url, person_id=oid)
        return self._get(url)
