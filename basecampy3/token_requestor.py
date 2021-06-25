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
    def __init__(self, client_id, redirect_uri=None, session=None, listen_addr=None):
        """
        For completing the OAuth2 authorization flow.

        :param client_id: the client ID of the integration you created
        :type client_id: str
        :param redirect_uri: the URL to redirect to as part of the flow (this is http://localhost:33333 by default)
        :type redirect_uri: str
        :param session: optionally provide your own Session object
        :type session: requests.sessions.Session
        :param listen_addr: the address to listen on. Usually this is localhost. It can also be set with the
            BC3_OAUTH_BIND_ADDRESS environment variable
        :type listen_addr: str
        """
        if redirect_uri is None:
            redirect_uri = constants.DEFAULT_REDIRECT_URI

        if not redirect_uri.lower().startswith("http"):
            raise ValueError("'%s' is an invalid Redirect URI. Should be a valid http(s) URL." % redirect_uri)

        if session is None:
            session = _create_session()

        if not listen_addr:
            listen_addr = constants.OAUTH_LOCAL_BIND_ADDRESS

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._session = session
        self._listen_addr = listen_addr

    def get_authorization(self):
        """
        Open the user's web browser to complete signing in and allow access. Spawn a local HTTP server to handle the
        redirect URI.
        :return:
        """
        quoted_uri = quote(self.redirect_uri)
        url = constants.AUTHORIZE_URL.format(client_id=self.client_id, redirect_uri=quoted_uri)
        print("Attempting to open a browser...")
        print("(You may have to copy/paste this into your web browser)\n%s" % url)
        webbrowser.open(url)
        parsed = urlparse(self.redirect_uri)
        listen_port = parsed.port
        if listen_port is None:
            listen_port = 80 if parsed.scheme == "http" else 443
        user_code = oauth_server.wait_for_user_response(self._listen_addr, listen_port)
        return user_code
