"""
A scraper that uses your username and password, in addition to your own app's client ID, client secret, and
redirect URI, to log in to Basecamp 3 as you and authorize your own app. This is how we can obtain an access token and
refresh token using your username and password. The request URI doesn't have to be a real URL but it does have to match
what you put as your app's redirect URI.
"""

from bs4 import BeautifulSoup
import requests
try:
    from urlparse import urljoin, urlparse, parse_qs
except ImportError:
    from urllib.parse import urljoin, urlparse, parse_qs


class TokenRequester(object):
    DOMAIN = "launchpad.37signals.com"

    # the authorization page for an app. (i.e. "Allow this app to access your data?")
    AUTH_URL = "https://{domain}/authorization/new?client_id={client_id}&redirect_uri={redirect_uri}&type=web_server"

    # pretend to be a browser
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/65.0.3325.181 Safari/537.36"

    def __init__(self, client_id, redirect_uri, user_email, user_pass, session=None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.user_email = user_email
        self.user_pass = user_pass
        self._session = session

    def get_user_code(self):
        # check that we have the needed fields in our configuration to do this...
        errors = []
        if self.client_id is None:
            errors.append('client_id')
        if self.redirect_uri is None:
            errors.append('redirect_uri')
        if self.user_email is None:
            errors.append('user_email')
        if self.user_pass is None:
            errors.append('user_pass')
        if errors:
            raise ValueError("The following required fields to get an access token are missing: %s" % ", ".join(errors))

        if self._session is None:
            self._session = requests.session()

        # log in to Basecamp 3 using the username and password like a browser
        login_resp = self._use_login_form(self.client_id, self.redirect_uri, self.user_email, self.user_pass)
        # TODO do something if this login was unsuccessful

        # if successful, we're on the authorize this app page for the client ID provided
        user_code = self._submit_authorize_app_form(login_resp.url, login_resp.text)
        # TODO do something if this didn't get us a code

        return user_code

    def _use_login_form(self, client_id, redirect_uri, user_email, user_pass):
        # get the page
        auth_url = self.AUTH_URL.format(domain=self.DOMAIN, client_id=client_id, redirect_uri=redirect_uri)
        resp = self._session.get(auth_url)

        # use Beautiful Soup to find the login form and the fields on it
        soup = BeautifulSoup(resp.text, 'html.parser')
        login_form = soup.find('form', attrs={'data-behavior': 'login_form'})
        action_url = login_form.attrs['action']
        login_data = {
            'username': user_email,
            'password': user_pass,
            'utf8': "\u2713",  # checkmark
            'remember_me': 'true',
            'commit': 'Log in',
        }
        # authenticity_token appears to be a CSRF token on the form, not related to the Oauth2 tokens we're seeking
        login_data['authenticity_token'] = login_form.find('input', attrs={'name': 'authenticity_token'}).attrs['value']

        post_login_url = urljoin(auth_url, action_url)  # the URL to send the login form data to (form's action)
        login_resp = self._session.post(post_login_url, data=login_data)

        return login_resp

    def _submit_authorize_app_form(self, url, html):
        authorize_app_page = BeautifulSoup(html, 'html.parser')
        auth_form = authorize_app_page.find('form')
        authorize_data = {}
        for finput in auth_form.find_all('input'):
            authorize_data[finput.attrs['name']] = finput.attrs.get('value')
        auth_form_url = auth_form.attrs['action']
        authorize_post_url = urljoin(url, auth_form_url)
        app_token_resp = self._session.post(authorize_post_url, data=authorize_data, allow_redirects=False)

        # the redirect has a "code" on the end. This is what authorizes us to get the access_token
        app_redirect_uri = app_token_resp.headers['Location']
        # parse the code out of the redirect URI
        auth_code = parse_qs(urlparse(app_redirect_uri).query)['code'][0]

        return auth_code
