import requests
from . import constants, oauth_server
from .bc3_api import _create_session
try:
    # noinspection PyCompatibility
    from urlparse import urljoin, urlparse, parse_qs
    from urllib import quote
except ImportError:
    # noinspection PyCompatibility
    from urllib.parse import urljoin, urlparse, parse_qs, quote
import webbrowser


class TokenRequester(object):
    def __init__(self, client_id, redirect_uri=None, session=None):
        """
        For completing the OAuth2 authorization flow.

        :param client_id: the client ID of the integration you created
        :type client_id: str
        :param redirect_uri: the URL to redirect to as part of the flow (this is http://localhost:33333 by default)
        :type redirect_uri: str
        :param session: optionally provide your own Session object
        :type session: requests.sessions.Session
        """
        if redirect_uri is None:
            redirect_uri = "http://localhost:%s/" % constants.OAUTH_LOCAL_BIND_PORT

        if session is None:
            session = _create_session()

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._session = session

    def get_authorization(self):
        """
        Open the user's web browser to complete signing in and allow access. Spawn a local HTTP server to handle the
        redirect URI.
        :return:
        """
        redirect_uri = quote(self.redirect_uri)
        url = constants.AUTHORIZE_URL.format(client_id=self.client_id, redirect_uri=redirect_uri)
        print("Opening browser window to:\n%s" % url)
        webbrowser.open(url)
        listen_port = urlparse(self.redirect_uri).port
        if listen_port is None:
            listen_port = 80
        user_code = oauth_server.wait_for_user_response(listen_port)
        return user_code
