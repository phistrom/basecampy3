"""
The only object you should have to import. Access all of the API from here.
"""
from datetime import datetime
import dateutil.parser
import logging
import requests
from .transport_adapter import Basecamp3TransportAdapter
import traceback

from basecampy3.exc import *
from .config import BasecampConfig
from .token_requestor import TokenRequester
from .endpoints import campfires
from .endpoints import campfire_lines
from .endpoints import messages
from .endpoints import message_boards
from .endpoints import message_categories
from .endpoints import people
from .endpoints import projects
from .endpoints import project_constructions
from .endpoints import templates
from .endpoints import todolists
from .endpoints import todolist_groups
from .endpoints import todos
from .endpoints import todosets


class Basecamp3(object):
    OAUTH_DOMAIN = "launchpad.37signals.com"
    ACCESS_TOKEN_URL = "https://{domain}/authorization/token?type=web_server&client_id={client_id}&" \
                       "redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
    REFRESH_TOKEN_URL = "https://{domain}/authorization/token?type=refresh&refresh_token={0.refresh_token}&" \
                        "client_id={0.client_id}&redirect_uri={0.redirect_uri}&client_secret={0.client_secret}"
    USER_AGENT = "My Test Python API (phillip@4stromberg.com)"

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, access_token=None, access_expires=None,
                 refresh_token=None, user_email=None, user_pass=None, conf=None):
        """
        Create a new Basecamp 3 API connection. The following combinations of parameters are valid:

        1. `access_token` only
            Can access the API for now, but when this `access_token` expires you'll have to provide a new one. Not
            ideal for automation.
        2. `refresh_token`
            With `client_id`, `client_secret`, `redirect_uri`, and a `refresh_token`, we can obtain and refresh our
            own `access_token`. `refresh_token`s don't seem to have a limit so this is ideal for automation.
        3. `user_email` and `user_pass`
            With `user_email`, `user_pass`, `client_id`, `client_secret`, and `redirect_uri`, we can obtain our own
            `refresh_token` and therefore our own `access_token`. This is ideal for first runs. If your configuration
            file is in a writable spot, your `access_token` and `refresh_token` can be written to it automatically.
            Once you have obtained a `refresh_token`, you should remove your `user_email` and `user_pass` from the
            configuration and then change your password on Basecamp's site as a best practice.

        `client_id`, `client_secret`, and `redirect_uri` can be obtained by creating a new app here:
            https://launchpad.37signals.com/integrations

        `redirect_uri` doesn't have to be a real URL, but it does have to match what you put when you registered your
        app at the site above.

        `access_token` and `refresh_token` are normally obtained when a user clicks your app integration page and
        presses the big green "Yes, I'll allow access" button, which redirects them to your `redirect_uri` with a
        authorization code attached to it. Your app then uses its client_secret and client_id to obtain the tokens with
        this authorization code. Since that is a long and confusing process that requires you to set up a web server
        to answer the `redirect_uri`, see below on how this API makes it easy to obtain.

        `user_email` and `user_pass` is a login for Basecamp. It is NOT recommended to use this long term. If your
        Basecamp configuration file is in a writeable location, this API will write the `access_token` and
        `refresh_token` to it. You can then delete your username and password from the configuration file. Refresh
        tokens have no limit. There is no reason to continue using your username and password once you have obtained it.

        :param client_id: your app's client_id is given to you when you create a new app
        :type client_id: str
        :param client_secret: your app's client_secret is given to you when you create a new app
        :type client_secret: str
        :param redirect_uri: your app's redirect_uri can be fake but it needs to match on your app page
        :type redirect_uri: str
        :param access_token: an access token you have obtained from a user
        :type access_token: str
        :param access_expires: (optional) when the access token will expire as a datetime or datetime.timestamp float
        :type access_expires: datetime.datetime|float
        :param refresh_token: a refresh token obtained from a user, used for obtaining a new access_token
        :type refresh_token: str
        :param user_email: a user's login email for Basecamp 3. Only used to obtain refresh_token.
        :type user_email: str
        :param user_pass: a user's login password for Basecamp 3. Only used to obtain refresh_token.
        :type user_pass: str
        :param conf: a BasecampConfig object with all the settings we need so that we don't have to fill out all
                         these parameters
        :type conf: basecampy3.config.BasecampConfig
        """
        can_request_our_own_refresh_tokens = client_id and client_secret and redirect_uri and user_email and user_pass
        can_refresh_access_tokens = refresh_token and client_id and client_secret and redirect_uri
        if access_token or can_refresh_access_tokens or can_request_our_own_refresh_tokens:
            conf = BasecampConfig(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                  user_email=user_email, user_pass=user_pass, access_token=access_token,
                                  refresh_token=refresh_token, access_expires=access_expires)
        elif conf is None:
            conf = BasecampConfig.load_from_default_paths()
        else:
            raise ValueError("Need a valid BasecampConfig object, a refresh token, an access token, or enough "
                             "information to get our own refresh tokens (client_id, client_secret, redirect_uri, "
                             "username, and password)")

        self._conf = conf
        self._session = requests.session()
        self._session.mount("https://", adapter=Basecamp3TransportAdapter())
        self._session.headers['User-Agent'] = self.USER_AGENT
        self.account_id = None
        self._authorize()
        self.campfires = campfires.Campfires(self)
        self.campfire_lines = campfire_lines.CampfireLines(self)
        self.messages = messages.Messages(self)
        self.message_boards = message_boards.MessageBoards(self)
        self.message_categories = message_categories.MessageCategories(self)
        self.people = people.People(self)
        self.projects = projects.Projects(self)
        self.project_constructions = project_constructions.ProjectConstructions(self)
        self.templates = templates.Templates(self)
        self.todolists = todolists.TodoLists(self)
        self.todolist_groups = todolist_groups.TodoListGroups(self)
        self.todos = todos.Todos(self)
        self.todosets = todosets.TodoSets(self)

    @property
    def who_am_i(self):
        data = self._get_data("https://%s/authorization.json" % self.OAUTH_DOMAIN)
        return data.json()

    @classmethod
    def trade_user_code_for_access_token(cls, client_id, redirect_uri, client_secret, code, session=None):
        access_token_url = cls.ACCESS_TOKEN_URL.format(domain=cls.OAUTH_DOMAIN, client_id=client_id,
                                                       redirect_uri=redirect_uri, client_secret=client_secret,
                                                       code=code)
        if session is None:
            session = requests.session()
        resp = session.post(access_token_url)  # this should be a JSON response with our access and refresh tokens
        if not resp.ok:
            raise InvalidUserCodeError(response=resp)

        token_json = resp.json()  # the None values should be replaced with the JSON values now
        return token_json

    def _get_data(self, url, auto_reauthorize=True):
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
            raise UnauthorizedError(message="Unable to authorize ourselves to Basecamp.", response=resp)
        return resp

    def _authorize(self):
        """
        Determine if we have the credentials at our disposal to make API calls.
        :return:
        """

        if self._is_token_expired():
            self._get_access_token()
        self._apply_token_to_headers()  # set our access token to the Authorization header for this session
        self.account_id = self._get_account_id()  # set our Basecamp account ID used in many API calls

    def _apply_token_to_headers(self):
        self._session.headers['Authorization'] = 'Bearer %s' % self._conf.access_token

    def _get_access_token(self):
        if self._conf.refresh_token:
            try:
                token_json = self._refresh_access_token()
                self._save_token_json(token_json)
                return  # if there wasn't an error, the access token is ready to go
            except InvalidRefreshTokenError:
                self._conf.refresh_token = None  # this is a bad token

        token_req = TokenRequester(self._conf.client_id, self._conf.redirect_uri,
                                   self._conf.user_email, self._conf.user_pass)
        code = token_req.get_user_code()

        token_json = self.trade_user_code_for_access_token(client_id=self._conf.client_id,
                                                           redirect_uri=self._conf.redirect_uri,
                                                           client_secret=self._conf.client_secret, code=code)
        self._save_token_json(token_json)

    def _get_account_id(self):
        identity = self.who_am_i
        for acct in identity['accounts']:
            if acct['product'] == 'bc3':
                return acct['id']
        raise UnknownAccountIDError("Could not determine this Basecamp account's ID")

    def _is_token_expired(self):
        """
        Check the access token in our configuration and see if it's expired. If it is expired or there isn't an access
        token, return Trues
        :return: True if token is missing or expired, False if the token is still valid
        """
        if not self._conf.access_token:
            return True
        self._apply_token_to_headers()  # ok then lets apply this token to our session if it's not there already
        try:
            resp = self._get_data("https://%s/authorization.json" % self.OAUTH_DOMAIN, False)
        except Exception as ex:
            logging.debug("Token is expired: %s" % traceback.format_exc())
            return True
        expires_at = dateutil.parser.parse(resp.json()['expires_at'])
        expires_at = expires_at.replace(tzinfo=None)
        return datetime.utcnow() >= expires_at

    def _refresh_access_token(self):
        url = self.REFRESH_TOKEN_URL.format(self._conf, domain=self.OAUTH_DOMAIN)
        resp = self._session.post(url)
        if resp.status_code != 200:
            raise InvalidRefreshTokenError(response=resp)
        token_json = resp.json()

        return token_json

    def _save_token_json(self, token_json):
        if 'access_token' in token_json:
            self._conf.access_token = token_json['access_token']
        if 'refresh_token' in token_json:
            self._conf.refresh_token = token_json['refresh_token']
        if 'expires_in' in token_json:
            self._conf.access_expires = token_json['expires_in']
        self._conf.save()
