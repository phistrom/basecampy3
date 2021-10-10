"""
To complete the Oauth2 flow, a "code" is sent as a GET parameter to the redirect URI on the authorization page. This
module subclasses the basic built-in Python 3 HTTP server to listen on port 33333 of the localhost by default. When
running `bc3 configure`, this module listens for the code sent in the redirect, and can return it to the CLI so the CLI
can perform the final step of requesting access and refresh tokens from Basecamp 3 and storing them for later use.
"""
import six
from six.moves.urllib_parse import parse_qs, urlparse
from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class OAuthRequestHandler(BaseHTTPRequestHandler):
    """
    Obtain the "code" GET parameter when redirected from Basecamp's authorization page. Then set it
    in the server object that created this Handler so it can be retrieved when the server quits.
    """
    def do_GET(self):
        """
        Class methods of an HTTP Handler must be of the form do_VERB, where VERB is the HTTP verb to handle. In our
        case we just want to handle the local user's browser getting redirected to http://localhost?code=CODE and place
        the CODE part of the URL in a field that can be accessed after the HTTPServer object has exited.
        :return:
        """
        parsed_path = urlparse(self.path)
        query_string = parsed_path.query
        qs_dict = parse_qs(query_string)
        code = qs_dict["code"]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """<html>
        <head>
        <title>BasecamPY3 Authorized</title>
        </head>
        <body>
        <h1>Success</h1>
        <p>BasecamPY3 authorized. You can close this browser window and return to the command line.</p>
        </body>
        </html>
        """
        lines = "\n".join([line.strip() for line in html.split("\n")]).encode("utf-8")
        self.wfile.write(lines)
        if not isinstance(code, six.string_types):
            code = code[0]
        # presumably this is an instance of OAuthHTTPServer (it will still work even if it isn't)
        self.server._user_code = code


class OAuthHTTPServer(HTTPServer, object):
    """
    Extends HTTPServer by adding a field "user_code" that can be set by the child object and makes the
    default RequestHandlerClass the `OAuthRequestHandler` defined above.
    """
    def __init__(self, server_address, RequestHandlerClass=OAuthRequestHandler):
        """
        :param server_address: a tuple of the form (local_ip_address, listen_port)
        :type server_address: tuple[str, int]
        :param RequestHandlerClass: the class that will be instantiated for each request to handle the request
        :type RequestHandlerClass: type[OAuthRequestHandler]
        """
        self._user_code = None
        super(OAuthHTTPServer, self).__init__(server_address, RequestHandlerClass)

    @property
    def user_code(self):
        return self._user_code


def wait_for_user_response(listen_addr, listen_port):
    """
    Start a web server on localhost at the specified port and wait for a single request to come in. Return the
    "code" parameter after the redirect URI.
    :param listen_addr: the address to bind to for listening. For security reasons, this is best left at 127.0.0.1
    :type listen_addr: str
    :param listen_port: the port for this HTTP server to listen on
    :type listen_port: int
    :return: the code GET param from the redirect URI (the part after the question mark)
    :rtype: str
    """
    server_addr = (listen_addr, listen_port)
    # server = httpserver.HTTPServer(server_addr, OAuthRequestHandler)
    server = OAuthHTTPServer(server_addr, OAuthRequestHandler)
    server.handle_request()  # handle only one request (as opposed to "serve_forever")
    # this is the code that can be used to obtain an access and refresh token
    return server.user_code
