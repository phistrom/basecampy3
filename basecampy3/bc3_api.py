"""
The Basecamp3 class should be the only thing you need to import to access just about all the functionality you need.
"""
import logging
from datetime import datetime
import dateutil.parser
import pytz
import requests
from .transport_adapter import Basecamp3TransportAdapter

from . import config, constants, endpoints, exc, urls

logger = logging.getLogger(__name__)


def _create_session():
    session = requests.Session()
    session.headers["User-Agent"] = constants.USER_AGENT
    return session


class Basecamp3(object):
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None,
                 access_token=None, refresh_token=None, account_id=None,
                 conf=None, config_file=None, api_url=constants.API_URL):
        """
        Create a new Basecamp 3 API connection. The preferred method of using
        this API is to run `bc3 configure` from the command line first, then
        you do not need to pass any parameters into this constructor.

        Parameters are prioritized in this order:

        default file path < environment variables < provided filepath < provided config object < provided parameters
        1. Default file path: Without a configuration object (`conf`)
           or `config_file`, BasecamPY3 looks for configuration files in
           the default places. See the `config` module for details.
        2. Environment variables: override or supplement the values found in
           the default file locations.
        3. If `config_file` is specified, environment variables will be
           overriden or supplemented with the contents of this file.
           This location will be used to persist `access_token`s.
        4. If `conf` is provided, the previous configurations will be
           supplemented or overriden with values from this object.
           If `conf` is non-volatile storage (i.e. a file configuration
           object), this object will be used to persist `access_token`s.
        5. If parameters are provided (like `client_id`, `client_secret`,
           etc.), they override or supplement all previous configurations.

        Essentially, stick to one method of providing parameters for the
        most straightforward experience.

        Non-volatile storage is the most ideal so BasecamPY3 has somewhere to
        put `access_token`s it obtains by using `refresh_token`s.
        `access_token`s currently last 2 weeks.

        `client_id`, `client_secret`, and `redirect_uri` can be obtained by creating a new app here:
            https://launchpad.37signals.com/integrations

        :param client_id: your app's client_id is given to you when you create a new app
        :type client_id: str
        :param client_secret: your app's client_secret is given to you when you create a new app
        :type client_secret: str
        :param redirect_uri: your app's redirect_uri can be fake but it needs to match on your app page
        :type redirect_uri: str
        :param access_token: an access token you have obtained from a user
        :type access_token: str
        :param refresh_token: a refresh token obtained from a user, used for obtaining a new access_token
        :type refresh_token: str
        :param account_id: the account ID to use (used if the user belongs to multiple Basecamp 3 accounts)
        :type account_id: str|int
        :param conf: a BasecampConfig object
        :type conf: basecampy3.config.BasecampConfig
        :param config_file: path to a configuration file to use for this object
        :type config_file: str
        :param api_url: base URL to use for all API calls
        :type api_url: str
        """

        # config precedence (leftmost is overriden by values from the rightmost):
        # default file path < environment variables < provided filepath < provided config object < provided parameters

        env_conf = config.EnvironmentConfig()
        if not (config_file or conf):
            base_conf = config.BasecampFileConfig.load_from_default_paths(silent_fail=True)
            base_conf.merge(env_conf)
        else:
            base_conf = env_conf

        if config_file:
            # we merge in the contents of the file, then we swap in the file_conf
            # so it can be the persistent location to save to
            file_conf = config.BasecampFileConfig.from_filepath(config_file)
            base_conf.merge(file_conf)
            file_conf.merge(base_conf)
            base_conf = file_conf

        if conf:
            base_conf.merge(conf)
            if conf.is_persistent:
                # if the user-provided configuration object is persistent,
                # make it our base_conf so we can persist our settings to it
                conf.merge(base_conf)
                base_conf = conf

        # parameters directly passed into the constructor
        args_conf = config.BasecampMemoryConfig(
            client_id=client_id, client_secret=client_secret,
            redirect_uri=redirect_uri, access_token=access_token,
            refresh_token=refresh_token, account_id=account_id
        )

        base_conf.merge(args_conf)

        if not base_conf.is_usable:  # user didn't provide enough fields in constructor
            raise ValueError("Unable to find a suitable Basecamp 3 configuration. Try running `bc3 configure`.")

        self._conf = base_conf
        session = _create_session()
        session.mount("https://", adapter=Basecamp3TransportAdapter())
        self.session = self._session = session
        self._authorize()
        self.urls = urls.BasecampURLs(self.account_id, api_url)

        self.answers = endpoints.Answers(self)
        self.campfires = endpoints.Campfires(self)
        self.campfire_lines = endpoints.CampfireLines(self)
        self.messages = endpoints.Messages(self)
        self.message_boards = endpoints.MessageBoards(self)
        self.message_categories = endpoints.MessageCategories(self)
        self.people = endpoints.People(self)
        self.projects = endpoints.Projects(self)
        self.project_constructions = endpoints.ProjectConstructions(self)
        self.templates = endpoints.Templates(self)
        self.todolists = endpoints.TodoLists(self)
        self.todolist_groups = endpoints.TodoListGroups(self)
        self.todos = endpoints.Todos(self)
        self.todosets = endpoints.TodoSets(self)

    @classmethod
    def from_environment(cls):
        """
        Alternative constructor that takes the authorization data from environment variables:

        - BASECAMP_CLIENT_ID
        - BASECAMP_CLIENT_SECRET
        - BASECAMP_REDIRECT_URL
        - BASECAMP_ACCESS_TOKEN
        - BASECAMP_REFRESH_TOKEN
        - BASECAMP_ACCOUNT_ID
        """
        conf = config.EnvironmentConfig()

        return cls(conf=conf)

    @property
    def who_am_i(self):
        """
        Get JSON that shows who we're logged in as

        :return: a dict with current user data
        """
        data = self._get_data(constants.AUTHORIZATION_JSON_URL, False)
        return data.json()

    @property
    def accounts(self):
        identity = self.who_am_i
        for acct in identity['accounts']:
            if acct['product'] == 'bc3':
                yield acct

    @classmethod
    def trade_user_code_for_access_token(cls, client_id, redirect_uri, client_secret, code, session=None):
        """
        Used during `bc3 configure` to interactively obtain an access_token and refresh_token from Basecamp.

        :param client_id: your integration's Client ID
        :type client_id: str
        :param redirect_uri: your integration's Redirect URI
        :type redirect_uri: str
        :param client_secret: your integration's Client Secret
        :type client_secret: str
        :param code: when a user clicks the "Allow" button in their browser on the authorization screen, they are
                        redirected to your Redirect URI with this code appended as ?code=CODE
        :type code: str
        :param session: optionally specify your own Session object
        :type session: requests.Session
        :return: a dictionary representation of the JSON response from the authorization endpoint
        :rtype: dict
        """
        access_token_url = constants.ACCESS_TOKEN_URL.format(client_id=client_id, redirect_uri=redirect_uri,
                                                             client_secret=client_secret, code=code)
        if session is None:
            session = _create_session()
        resp = session.post(access_token_url)  # this should be a JSON response with our access and refresh tokens
        if not resp.ok:
            raise exc.InvalidUserCodeError(response=resp)

        token_json = resp.json()  # the None values should be replaced with the JSON values now
        return token_json

    def _get_data(self, url, auto_reauthorize=True):
        """
        Perform a GET request with automatic reauthorizations if the access_token has expired.

        :param url: the URL to send a GET request to
        :type url: str
        :param auto_reauthorize: whether to automatically try to re-authorize on a 401 Unauthorized response
        :type auto_reauthorize: bool
        :return: the Response object
        :rtype: requests.Response
        """
        times_to_try = 2 if auto_reauthorize else 1
        resp = None
        for attempt in range(0, times_to_try):
            resp = self._session.get(url)
            if resp.status_code == 401 and auto_reauthorize:
                if attempt == (times_to_try - 1):  # was our last attempt
                    break
                else:
                    self._authorize()  # reauthorize
                    continue
            break  # we were authorized so we can stop attempting

        code = resp.status_code

        if code == 401:
            raise exc.UnauthorizedError(message="Unable to authorize ourselves to Basecamp.", response=resp)
        return resp

    def _authorize(self):
        """
        Determine if we have the credentials at our disposal to make API calls.
        :return:
        """

        if self._is_token_expired():
            self._get_access_token()
        self.account_id = self._get_account_id()  # set our Basecamp account ID used in many API calls

    def _apply_token_to_headers(self):
        self._session.headers['Authorization'] = 'Bearer %s' % self._conf.access_token

    def _get_access_token(self):
        """
        Use our refresh_token to get a new access_token. This updates our BasecampConfig object with the new values.
        """
        if not self._conf.refresh_token:
            raise exc.InvalidRefreshTokenError(message="No refresh_token provided. Cannot obtain a new access_token.")
        try:
            token_json = self._refresh_access_token()
            if 'access_token' in token_json:
                self._conf.access_token = token_json['access_token']
                self._apply_token_to_headers()
            if 'refresh_token' in token_json:
                self._conf.refresh_token = token_json['refresh_token']
            self._conf.save()
        except exc.InvalidRefreshTokenError as ex:
            self._conf.refresh_token = None  # this is a bad token
            raise ex

    def _get_account_id(self):
        """
        Get the account ID for this user. Returns the first account ID found where the product field is "bc3".
        :return: str
        """

        if self._conf.account_id:
            return self._conf.account_id

        identity = self.who_am_i
        accounts = [acct for acct in identity['accounts'] if acct['product'] == 'bc3']
        if len(accounts) == 1:
            return accounts[0]['id']
        elif len(accounts) < 1:
            raise exc.UnknownAccountIDError("You do not belong to any Basecamp 3 accounts.")
        else:
            account = accounts[0]
            logger.warning("You belong to more than one Basecamp3 account and you do not have an account_id \n"
                           "specified in your configuration. Please run `bc3 configure` again to avoid this warning. \n"
                           "Proceeding with legacy behavior of picking the first account which is %s (ID = %s)..." %
                           (account['name'], account['id']))
            return account['id']

    def _is_token_expired(self):
        """
        Check the access token in our configuration and see if it's expired. If it is expired or there isn't an access
        token, return Trues
        :return: True if token is missing or expired, False if the token is still valid
        """
        if not self._conf.access_token:
            return True
        self._apply_token_to_headers()  # apply our current access_token to our session if it's not there already
        data = self.who_am_i

        # the format of the expires_at date in the JSON response is ISO 8601
        # YYYY-mm-ddTHH:MM:SS.fffZ
        # We use dateutil's isoparse to get more easily/robustly parse the
        # string and make sure it has timezone data (even if it is just UTC).
        expires_at = dateutil.parser.isoparse(data['expires_at'])
        # ensure it is UTC
        expires_at = expires_at.astimezone(pytz.utc)
        now = pytz.utc.localize(datetime.utcnow())
        return now >= expires_at

    def _refresh_access_token(self):
        url = constants.REFRESH_TOKEN_URL.format(self._conf)
        resp = self._session.post(url)
        if resp.status_code != 200:
            raise exc.InvalidRefreshTokenError(response=resp)
        token_json = resp.json()

        return token_json
