"""
Constants used throughout the basecampy3 package. Some constants are assigned by environment variables at startup.
"""

from .__version__ import __version__
import os

API_URL = "https://3.basecampapi.com/"

OAUTH_URL = "https://launchpad.37signals.com"

OAUTH_LOCAL_BIND_ADDRESS = os.getenv("BC3_OAUTH_BIND_ADDRESS", "127.0.0.1")
"""A web server will bind to this address when authorizing your oauth tokens in `bc3 configure`. If running in a 
container, you may need to set this to 0.0.0.0 to listen to 'external' connections from the host (i.e. you)"""

OAUTH_LOCAL_BIND_PORT = 33333
"""A web server will bind to this port on OAUTH_LOCAL_BIND_ADDRESS when authorizing your oauth tokens 
in `bc3 configure`"""

DEFAULT_REDIRECT_URI = "http://localhost:%d" % OAUTH_LOCAL_BIND_PORT
"""The default Redirect URI recommended for your Basecamp 3 OAuth2 integration. This should always be localhost"""

AUTHORIZE_URL = "%s/authorization/new?" \
                "client_id={client_id}&redirect_uri={redirect_uri}&type=web_server" % OAUTH_URL
"""Confirms you want to allow an app (identified by client_id) to have access to your Basecamp 3 account"""

AUTHORIZATION_JSON_URL = "%s/authorization.json" % OAUTH_URL

ACCESS_TOKEN_URL = "%s/authorization/token?type=web_server&client_id={client_id}&" \
                       "redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}" % OAUTH_URL
"""Using the code received during initial authentication, obtain access and refresh tokens."""

REFRESH_TOKEN_URL = "%s/authorization/token?type=refresh&refresh_token={0.refresh_token}&" \
                    "client_id={0.client_id}&redirect_uri={0.redirect_uri}&client_secret={0.client_secret}" % OAUTH_URL
"""Using a saved refresh token, apply for new access token."""

_user_default_config_dir = os.getenv("BC3_CONFIG_PATH")
if _user_default_config_dir:
    DEFAULT_CONFIG_FILE = _user_default_config_dir
else:
    _home_config = os.path.expanduser(os.path.join("~", ".config"))
    # in case the user has a special place for config files:
    _default_config_dir = os.getenv("XDG_CONFIG_HOME", _home_config)
    DEFAULT_CONFIG_FILE = os.path.join(_default_config_dir, "basecamp.conf")

DOCK_NAME_CAMPFIRE = 'chat'
DOCK_NAME_MESSAGE_BOARD = 'message_board'
DOCK_NAME_TODOS = 'todoset'
DOCK_NAME_SCHEDULE = 'schedule'
DOCK_NAME_CHECKIN = 'questionnaire'
DOCK_NAME_VAULT = 'vault'
DOCK_NAME_FORWARDS = 'inbox'

DATE_FORMAT = "%a %b %d %Y %H:%M:%S GMT%z"

RATE_LIMIT_REQUESTS = 50
RATE_LIMIT_PER_SECONDS = 10

VERSION = __version__

USER_AGENT = "BasecamPY3 {version} (https://github.com/phistrom/basecampy3)".format(version=VERSION)
