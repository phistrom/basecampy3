from ._base import BasecampEndpoint, BasecampObject
import six


@six.python_2_unicode_compatible
class Template(BasecampObject):
    """
    A Project Template or Blueprint from which you can make Projects that have the same start.
    """

    def create_project(self, name, description=""):
        return self._endpoint._api.project_constructions.create_project(self, name, description)

    def trash(self):
        return self._endpoint.trash(self)

    def __int__(self):
        return int(self.id)

    def __str__(self):
        try:
            return u"Template {0.id}: '{0.name}'".format(self)
        except:
            return super(Template, self).__str__()

    def __repr__(self):
        repr_dict = {k: v for k, v in self._values.items() if k not in ("dock",)}
        return u"Template(%s)" % repr(repr_dict)


class Templates(BasecampEndpoint):
    OBJECT_CLASS = Template

    CREATE_URL = "{base_url}/templates.json"
    GET_URL = "{base_url}/templates/{template_id}.json"
    LIST_URL = "{base_url}/templates.json"
    UPDATE_URL = "{base_url}/templates/{template_id}.json"
    TRASH_URL = "{base_url}/templates/{template_id}.json"

    def create(self, name, description=""):
        data = {
            'name': name,
            'description': description,
        }
        url = self.CREATE_URL.format(base_url=self.url)
        new_template = self._create(url, data=data)
        return new_template

    def get(self, template):
        """
        Get just one Template.

        :param template: a Template object or ID
        :return: a Template object if found, raises an error if not found
        """
        template = int(template)
        url = self.GET_URL.format(base_url=self.url, template_id=template)
        return self._get(url)

    def list(self, status=None):
        """
        Get a list of Basecamp Project Templates visible to the user.

        :param status: optionally can be 'archived' or 'trashed' to get templates of that type
        :return: a list of Template objects
        """
        params = {}
        if status is not None:
            params['status'] = status
        url = self.LIST_URL.format(base_url=self.url)
        return self._get_list(url, params)

    def update(self, template, name=False, description=False):
        """
        Change the given Template's name and/or description.

        :param template: a Template object or ID
        :param name: the new name for this Template. A value of False means no change.
        :param description: the new description for this Template. A value of False means no change.
        """
        if name is False and description is False:
            raise ValueError("Nothing to update for Template %s" % template)
        template = int(template)
        data = {}
        if name is not False:
            data['name'] = name
        if description is not False:
            data['description'] = description
        url = self.UPDATE_URL.format(base_url=self.url, template_id=template)
        self._update(url, data=data)

    def trash(self, template):
        template = int(template)
        url = self.TRASH_URL.format(base_url=self.url, template_id=template)
        self._delete(url)



