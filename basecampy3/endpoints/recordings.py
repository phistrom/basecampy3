from . import _base, projects, util


class Recording(_base.BasecampObject):
    """
    Most of the data structures in the Basecamp 3 API are represented as "Recordings", with generic actions
    available to be performed.

    See also:
    https://github.com/basecamp/bc3-api/blob/master/sections/recordings.md
    """
    @property
    def project_id(self):
        """
        :return: the ID of the Project this Recording belongs to.
        :rtype:  int
        """
        return int(self._values['bucket']['id'])

    def archive(self):
        """
        Archive this Recording.
        """
        self._endpoint.archive(project=self.project_id, recording=self)

    def unarchive(self):
        """
        Unarchive this Recording.
        """
        self._endpoint.unarchive(project=self.project_id, recording=self)

    def trash(self):
        """
        Trash this Recording. Trashed items are automatically deleted permanently after 30 days.
        """
        self._endpoint.trash(project=self.project_id, recording=self)


class RecordingEndpoint(_base.BasecampEndpoint):
    OBJECT_CLASS = Recording

    ARCHIVE_URL = "{base_url}/buckets/{project_id}/recordings/{recording_id}/status/archived.json"
    UNARCHIVE_URL = "{base_url}/buckets/{project_id}/recordings/{recording_id}/status/active.json"
    TRASH_URL = "{base_url}/buckets/{project_id}/recordings/{recording_id}/status/trashed.json"

    def archive(self, project=None, recording=None):
        """
        Archive a Recording given its Project and Recording ID.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param recording: a Recording object or ID
        :type recording: Recording|int
        """
        project_id, recording_id = util.project_or_object(project, recording)
        url = self.ARCHIVE_URL.format(base_url=self.url, project_id=project_id, recording_id=recording_id)
        self._no_response(url, method="PUT")

    def unarchive(self, project=None, recording=None):
        """
        Unarchive this Record object.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param recording: a Recording object or ID
        :type recording: Recording|int
        """
        project_id, recording_id = util.project_or_object(project, recording)
        url = self.UNARCHIVE_URL.format(base_url=self.url, project_id=project_id, recording_id=recording_id)
        self._no_response(url, method="PUT")

    def trash(self, project=None, recording=None):
        """
        Trash the given Recording. Trashed items are automatically deleted permanently after 30 days.

        :param project: a Project object or ID
        :type project: basecampy3.endpoints.projects.Project|int
        :param recording: a Recording object or ID
        :type recording: Recording|int
        """
        project_id, recording_id = util.project_or_object(project, recording)
        url = self.TRASH_URL.format(base_url=self.url, project_id=project_id, recording_id=recording_id)
        self._no_response(url, method="PUT")
