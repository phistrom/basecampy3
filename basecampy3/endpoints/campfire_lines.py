from ._base import BasecampEndpoint, BasecampObject
from ..constants import DOCK_NAME_CAMPFIRE
from . import util


class CampfireLine(BasecampObject):
    """
    A single line of a Campfire. Basically, a single chat message.
    """
    def __int__(self):
        return int(self.id)

    def __str__(self):
        try:
            return "[{}] {}: '{}'".format(self.created_at, self.creator['name'], self.content)
        except:
            return super(CampfireLine, self).__str__()


class CampfireLines(BasecampEndpoint):
    OBJECT_CLASS = CampfireLine

    LIST_URL = "{base_url}/buckets/{project_id}/chats/{campfire_id}/lines.json"
    GET_URL = "{base_url}/buckets/{project_id}/chats/{campfire_id}/lines/{campfire_line_id}.json"
    CREATE_URL = "{base_url}/buckets/{project_id}/chats/{campfire_id}/lines.json"
    DELETE_URL = "{base_url}/buckets/{project_id}/chats/{campfire_id}/lines/{campfire_line_id}.json"

    def list(self, project=None, campfire=None):
        """
        Get a list of chat lines in the given Campfire.
        If `campfire` is a Campfire object, the `project` parameter can be omitted.
        If `project` is a Project object, the `campfire` parameter can be omitted.

        :param project: a Project object or Project ID
        :param campfire: a Campfire object or Campfire ID
        :return: a list of messages in the project
        """
        project_id, campfire_id = util.project_or_object(project, campfire, section_name=DOCK_NAME_CAMPFIRE)
        url = self.LIST_URL.format(base_url=self.url, project_id=project_id, campfire_id=campfire_id)
        return self._get_list(url)

    def get(self, campfire_line, project=None, campfire=None):
        """
        Get a single Campfire Line

        :param campfire_line: Campfire Line ID
        :param project: a Project object or Project ID
        :param campfire: a Campfire object or Campfire ID
        :return: a Campfire Line object
        """
        campfire_line = int(campfire_line)
        project_id, campfire_id = util.project_or_object(project, campfire, section_name=DOCK_NAME_CAMPFIRE)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, campfire_id=campfire_id,
                                  campfire_line_id=campfire_line)
        return self._get(url)

    def create(self, content, project=None, campfire=None):
        """
        Post a new line (message) in the given Campfire from the current user with the provided `content` string.
        Can be formatted in HTML.

        :param content: message string that can be HTML-formatted
        :param project: a Project object or Project ID
        :param campfire: a Campfire object or Campfire ID
        :return: the newly created Campfire Line
        """
        project_id, campfire_id = util.project_or_object(project, campfire, section_name=DOCK_NAME_CAMPFIRE)
        data = {
            'content': content,
        }
        url = self.CREATE_URL.format(base_url=self.url, project_id=project_id, campfire_id=campfire_id)
        new_line = self._create(url, data=data)
        return new_line

    def delete(self, campfire_line, project=None, campfire=None):
        """
        Delete a line from the campfire.

        :param campfire_line: the Campfire Line object or ID
        :param project: a Project object or Project ID
        :param campfire: a Campfire object or Campfire ID
        """
        campfire_line = int(campfire_line)
        project_id, campfire_id = util.project_or_object(project, campfire, section_name=DOCK_NAME_CAMPFIRE)
        url = self.DELETE_URL.format(base_url=self.url, project_id=project_id, campfire_id=campfire_id,
                                     campfire_line_id=campfire_line)
        self._delete(url)
