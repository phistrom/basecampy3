from ._base import BasecampObject, BasecampEndpoint
from ..constants import DOCK_NAME_CAMPFIRE
from . import util


class Campfire(BasecampObject):
    def __int__(self):
        return int(self.id)

    @property
    def lines(self):
        """
        Get the messages posted in this Campfire. Messages are known as "lines" so they don't get confused with
        Campfire's Message Board.
        :return: the CampfireLine objects in this Campfire
        :rtype: collections.Iterable[basecampy3.endpoints.campfire_lines.CampfireLine]
        """
        return self._endpoint._api.campfire_lines.list(campfire=self)

    @property
    def project(self):
        """
        Get the Project object this Campfire belongs to
        :return: the Project object this Campfire belongs to
        """
        if self.bucket['type'] == 'Project':
            return self._endpoint._api.projects.get(self.bucket['id'])
        return None

    def post_message(self, content):
        """
        Post a new line (message) in this campfire from the current user with the provided `content` string.
        Can be formatted in HTML.

        :param content: message string that can be HTML-formatted
        :type content: str
        :return: the new CampfireLine object
        :rtype: basecampy3.endpoints.campfire_lines.CampfireLine
        """
        return self._endpoint._api.campfire_lines.create(content, campfire=self)

    def __str__(self):
        return "Campfire %s: '%s'" % (self.id, self.bucket['name'])


class Campfires(BasecampEndpoint):
    OBJECT_CLASS = Campfire

    GET_URL = "{base_url}/buckets/{project_id}/chats/{campfire_id}.json"
    LIST_URL = "{base_url}/chats.json"

    def get(self, project=None, campfire=None):
        """
        Get just one campfire by its ID and a Project's ID. Provide a Project object or Campfire to skip
        the other parameter (i.e. if you pass a Campfire object, you do not need to specify the project parameter)

        :param campfire: the Campfire or Campfire's ID
        :param project: the Project object or Project's ID

        :return: a Campfire object if found, raises an error if not found
        """
        project_id, campfire_id = util.project_or_object(project, campfire, section_name=DOCK_NAME_CAMPFIRE)
        url = self.GET_URL.format(base_url=self.url, project_id=project_id, campfire_id=campfire_id)
        return self._get(url)

    def list(self):
        """
        Get a list of all active Campfires visible to the current user.

        :return: a list of Campfire objects
        """
        url = self.LIST_URL.format(base_url=self.url)
        return self._get_list(url)

