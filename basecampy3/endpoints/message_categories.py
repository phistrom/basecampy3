from ._base import BasecampObject, BasecampEndpoint


class MessageCategory(BasecampObject):
    def edit(self, project, name=False, icon=False):
        """
        Edit the MessageCategory, changing its name, its icon, or both.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param name: the new name for this category or False for no change
        :type name: str
        :param icon: the new icon for this category or False for no change
        :type icon: str
        """
        self._endpoint.update(project=project, category=self, name=name, icon=icon)

    def delete(self, project):
        self._endpoint.delete(project=project, category=self)

    def __int__(self):
        return int(self.id)

    def __str__(self):
        try:
            return "MessageCategory {0.id}: '{0.name}' {0.icon}".format(self)
        except:
            return super(MessageCategory, self).__str__()


class MessageCategories(BasecampEndpoint):
    OBJECT_CLASS = MessageCategory

    CREATE_URL = "{base_url}/buckets/{project_id}/categories.json"
    DELETE_URL = "{base_url}/buckets/{project_id}/categories/{category_id}.json"
    GET_URL = "{base_url}/buckets/{project_id}/categories/{category_id}.json"
    LIST_URL = "{base_url}/buckets/{project_id}/categories.json"
    UPDATE_URL = "{base_url}/buckets/{project_id}/categories/{category_id}.json"

    def create(self, name, icon, project):
        """

        :param name: the name of this MessageCategory
        :type name: str
        :param icon: the icon for this MessageCategory (usually the unicode character for an emoji)
        :type str: str
        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :return: the newly created MessageCategory object
        :rtype: MessageCategory
        """
        project = int(project)
        data = {
            "name": name,
            "icon": icon,
        }
        url = self.CREATE_URL.format(base_url=self.url, project_id=project)
        new_category = self._create(url, data=data)
        return new_category

    def delete(self, project, category):
        """
        Deletes the MessageCategory from the Project.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param category: a MessageCategory object or ID
        :type category: MessageCategory|int
        """
        project = int(project)
        category = int(category)
        url = self.DELETE_URL.format(base_url=self.url, project_id=project, category_id=category)
        self._delete(url)

    def get(self, project, category):
        """
        Get just one MessageCategory.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param category: a MessageCategory object or ID
        :type category: MessageCategory|int
        :return: a MessageCategory object if found, raises an error if not found
        :rtype: MessageCategory
        """
        project = int(project)
        category = int(category)
        url = self.GET_URL.format(base_url=self.url, project_id=project, category_id=category)
        return self._get(url)

    def list(self, project):
        """
        Get a list of Messages Categories from a given Project.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :return: a list of MessageCategory objects
        :rtype: collections.Iterable[MessageCategory]
        """
        project = int(project)
        url = self.LIST_URL.format(base_url=self.url, project_id=project)
        return self._get_list(url)

    def update(self, project, category, name=False, icon=False):
        """
        Change the name or icon of a given MessageCategory.
        False is a placeholder for no-change. None erases the value like a blank string.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param category: a MessageCategory object or ID
        :type category: MessageCategory|int
        :param name: change the name of the MessageCategory
        :type name: str
        :param icon: change the icon of the MessageCategory
        :type icon: str
        """
        if name is False and icon is False:
            raise ValueError("At least one of subject, content, and category parameters should have a value to "
                             "be changed.")
        project = int(project)
        category = int(category)

        data = {}
        if name is not False:
            data['name'] = "" if name is None else name
        if icon is not False:
            data['icon'] = "" if icon is None else icon

        url = self.UPDATE_URL.format(base_url=self.url, project_id=project, category_id=category)
        self._update(url, data=data)
