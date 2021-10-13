"""
The Basecamp3 class should be the only thing you need to import to access just about all the functionality you need.
"""
import logging
import os
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
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, access_token=None, refresh_token=None,
                 account_id=None, conf=None, api_url=constants.API_URL):
        """
        Create a new Basecamp 3 API connection. The following combinations of parameters are valid:

        1. `access_token` only
            Can access the API for now, but when this `access_token` expires you'll have to provide a new one. Not
            ideal for automation.
        2. `refresh_token`
            With `client_id`, `client_secret`, `redirect_uri`, and a `refresh_token`, we can obtain and refresh our
            own `access_token`. `refresh_token`s don't seem to have a limit so this is ideal for automation.
        3. `conf`
            Specify a BasecampConfig object instead of all the other parameters. This is the preferred method because
            then BasecamPY3 can potentially save new access tokens acquired by the refresh token to whatever
            persistence method backs the BasecampConfig.

        It is an error to specify conf with any other parameter.

        `client_id`, `client_secret`, and `redirect_uri` can be obtained by creating a new app here:
            https://launchpad.37signals.com/integrations

        `redirect_uri` doesn't have to be a real URL, but it does have to match what you put when you registered your
        app at the site above.

        `access_token` and `refresh_token` are normally obtained when a user clicks your app integration page and
        presses the big green "Yes, I'll allow access" button, which redirects them to your `redirect_uri` with a
        authorization code attached to it. Your app then uses its client_secret and client_id to obtain the tokens with
        this authorization code. Use `bc3 configure` from the command line to be guided through obtaining access and
        refresh tokens on behalf of your integration.

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
        :param conf: a BasecampConfig object with all the settings we need so that we don't have to fill out all
                         these parameters
        :type conf: basecampy3.config.BasecampConfig
        """
        has_direct_values = client_id or client_secret or redirect_uri or access_token or refresh_token
        if conf and has_direct_values:
            raise ValueError("You cannot specify a BasecampConfig object as well as direct values such as client_id or "
                             "redirect_uri")
        if has_direct_values:  # user provided fields in constructor
            conf = config.BasecampMemoryConfig(client_id=client_id, client_secret=client_secret,
                                               redirect_uri=redirect_uri, access_token=access_token,
                                               refresh_token=refresh_token, account_id=account_id)
            if not conf.is_usable:  # user didn't provide enough fields in constructor
                raise ValueError("Unable to use the Basecamp 3 API. Not enough information provided.")
        elif conf is None:  # user provided no fields at all, look for a saved config file (the preferred way to run)
            conf = config.BasecampFileConfig.load_from_default_paths()

        # if the user didn't provide a config or the config we found on disk is unusable, we have to quit
        if conf is None or not conf.is_usable:
            # pretty sure this is impossible. load_from_default_paths() raises an Exception if no config is found
            raise ValueError("Unable to find a suitable Basecamp 3 configuration. Try running `bc3 configure`.")

        self._conf = conf
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
        """
        env = os.environ
        return cls(
            client_id=env['BASECAMP_CLIENT_ID'],
            client_secret=env['BASECAMP_CLIENT_SECRET'],
            redirect_uri=env['BASECAMP_REDIRECT_URL'],
            access_token=env['BASECAMP_ACCESS_TOKEN'],
            refresh_token=env['BASECAMP_REFRESH_TOKEN']
        )

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
        expires_at = dateutil.parser.isoparse(data['expires_at'])
        expires_at = expires_at.astimezone(pytz.utc)  # just in case Basecamp 3 decides to stop being UTC
        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        return now >= expires_at

    def _refresh_access_token(self):
        url = constants.REFRESH_TOKEN_URL.format(self._conf)
        resp = self._session.post(url)
        if resp.status_code != 200:
            raise exc.InvalidRefreshTokenError(response=resp)
        token_json = resp.json()

        return token_json
