import six


@six.python_2_unicode_compatible
class Basecamp3Error(Exception):
    def __init__(self, response=None, message=None):
        super(Basecamp3Error, self).__init__()
        self.response = response
        self.message = message

    def __str__(self):
        if self.response is not None:
            return u"%s %s %s" % (self.response.status_code, self.response.reason, self.response.text)
        if self.message is not None:
            return self.message
        return type(self).__name__


class InvalidRefreshTokenError(Basecamp3Error):
    pass


class InvalidUserCodeError(Basecamp3Error):
    pass


class UnauthorizedError(Basecamp3Error):
    pass


class UnknownAccountIDError(Basecamp3Error):
    pass


class ProjectCreationTimedOutError(Basecamp3Error):
    pass


class NoDefaultConfigurationFound(Basecamp3Error):
    def __init__(self, response=None, message=None):
        super(NoDefaultConfigurationFound, self).__init__(response, message)
        self.message = "No default configuration could be found. Try running `bc3 configure` from the command line."
