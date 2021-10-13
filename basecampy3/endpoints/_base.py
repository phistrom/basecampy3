from ..exc import *
from . import util
from .. import constants
import abc
import re
import six
from six.moves.urllib_parse import urljoin


class BasecampObject(object):
    def __init__(self, json_dict, endpoint):
        """
        A Basecamp object retrieved from the API. The fields are stored in a special `_values` dictionary to
        accomodate future updates to the Basecamp 3 API. The fields inside the `_values` dictionary can be retrieved
        as if they were attributes of this object. Anything deeper than the first level object has to be done as a
        dictionary access.

        :param json_dict: a dictionary representing the parsed JSON returned by an API call
        :type json_dict: dict
        :param endpoint: a BasecampEndpoint for easy access to the Basecamp3 object that created this object
        :type endpoint: BasecampEndpoint
        """
        self._values = json_dict
        self._endpoint = endpoint

    def refresh(self, url=None):
        """
        Refresh this object's values from the API
        """
        if url is None:
            if 'url' in self._values:
                url = self._values['url']
            else:
                ex = ValueError("Can't refresh {object} without a URL".format(object=type(self).__name__))
                raise ex
        new_item = self._endpoint._get(url)  # luckily this object has the URL we can refresh from
        self._values.clear()
        self._values.update(new_item._values)

    def __getattr__(self, item):
        try:
            return self._values[item]
        except KeyError:
            # ex = "'{type}' object has no attribute '{item}'".format(type=self.__class__.__name__, item=item)
            ex = "'{type}' object has no attribute '{item}'".format(type='BasecampObject', item=item)
            raise AttributeError(ex)

    def __dir__(self):
        parent_dict = [a for a in super(BasecampObject, self).__dir__()]
        parent_dict.extend(self._values.keys())
        return parent_dict

    def __int__(self):
        return int(self.id)

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, repr(self._values))

    def __setattr__(self, key, value):
        if key in {"_values", "_endpoint"} or key not in self._values:
            return super(BasecampObject, self).__setattr__(key, value)
        else:
            self._values[key] = value

    def __str__(self):
        return "{type}".format(type=type(self).__name__)


@six.add_metaclass(abc.ABCMeta)
class RecordingBase(BasecampObject):
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


class BasecampEndpoint(object):
    OBJECT_CLASS = BasecampObject
    URL = constants.API_URL
    _LINK_HEADER_URL_REGEX = re.compile(r'<(https.+)>')

    def __init__(self, api):
        """
        :param api: the API object that handles authorization and HTTP requests
        :type api: basecampy3.bc3_api.Basecamp3
        """
        self._api = api
        self.url = urljoin(self.URL, "/%s" % api.account_id)

    def _get_list(self, url, params=None, method="GET"):
        """
        Basecamp 3's API returns a paginated list of elements for most GET list endpoints. It has a geared pagination
        ratio so page 1 has 15 objects, page 2 has 30, page 3 has 50, and pages 4 and up have 100 objects each. This
        function returns a generator that can be looped through. The next page is transparently fetched when a user's
        loop has exhausted the current page.

        Someone could probably re-write this in a way that grabbed the next page asynchronously ahead of time...

        :param url: the URL to GET a list from
        :type url: str
        :param params: the GET parameters to add to the url after the "?" like "/projects.json?key=value&key2=value2"
        :type params: dict
        :param method: the HTTP verb to use when fetching this URL. Usually "GET".
        :type method: str
        :return: a generator that produces the requested objects
        :rtype: collections.Iterable[BasecampObject]
        """
        request_args = {'method': method, 'url': url}
        if params is not None:
            request_args['params'] = params

        return self._paginated_generator(request_args)

    def _get(self, url, method="GET"):
        resp = self._api._session.request(method, url)
        if not resp.ok:
            raise Basecamp3Error(response=resp)
        item = resp.json()
        return self.OBJECT_CLASS(item, self)

    def _create(self, url, data, method="POST", object_class=None):
        resp = self._api._session.request(method, url, json=data)
        if not resp.ok:
            raise Basecamp3Error(response=resp)
        json_data = resp.json()
        if object_class is None:
            object_class = self.OBJECT_CLASS
        item = object_class(json_data, self)
        return item

    def _update(self, url, data, method="PUT"):
        resp = self._api._session.request(method, url, json=data)
        if not resp.ok:
            raise Basecamp3Error(response=resp)
        json_data = resp.json()
        item = self.OBJECT_CLASS(json_data, self)
        return item

    def _no_response(self, url, data=None, method="PUT"):
        request_args = {"url": url, "method": method}
        if data is not None:
            request_args['json'] = data
        resp = self._api._session.request(**request_args)
        if not resp.ok:
            raise Basecamp3Error(response=resp)

    def _delete(self, url, method="DELETE"):
        resp = self._api._session.request(method, url)
        if not resp.ok:
            raise Basecamp3Error(response=resp)
        return resp

    def _paginated_generator(self, request_args):
        """
        Automatically gets the next page when getting paginated results, yielding each object on each page.

        :param request_args: kwargs for Session.request method
        :type request_args: dict
        """
        while request_args:
            resp = self._api._session.request(**request_args)
            if not resp.ok:
                raise Basecamp3Error(response=resp)
            link_header = resp.headers.get("Link")
            if link_header:
                next_page_url = self._LINK_HEADER_URL_REGEX.findall(link_header)[0]
                request_args = {'url': next_page_url, 'method': 'GET'}  # get ready to call the next page
            else:
                request_args = None  # clear it so we break the loop
            items_json = resp.json()
            for jdict in items_json:
                item = self.OBJECT_CLASS(jdict, self)  # convert JSON dict into a BasecampObject
                yield item


@six.add_metaclass(abc.ABCMeta)
class RecordingEndpointBase(BasecampEndpoint):
    OBJECT_CLASS = RecordingBase

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
