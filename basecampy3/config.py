"""
BasecampConfig and some built-in subclasses of it.
"""


import abc
import os
import six
from six.moves.configparser import ConfigParser, NoSectionError, NoOptionError

from . import constants, exc
from .log import logger


@six.add_metaclass(abc.ABCMeta)
class BasecampConfig(object):
    """
    Base configuration object for Basecamp3. Stores important tokens and info necessary to use the Basecamp 3 API.
    Subclass BasecampConfig when you would like to use your own persistent storage for configuration data. An in-memory
    and file class are provided out of the box.
    """
    FIELDS_TO_PERSIST = [
        "client_id",
        "client_secret",
        "redirect_uri",
        "access_token",
        "refresh_token",
        "account_id",
    ]
    """Fields that are expected to be persisted by the save function."""

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, access_token=None, refresh_token=None,
                 account_id=None):
        """
        :param client_id: the Client ID for the Basecamp 3 integration to use
        :type client_id: str
        :param client_secret: the Client Secret for the Basecamp 3 integration to use
        :type client_secret: str
        :param redirect_uri: the Redirect URI from the Basecamp 3 integration to use
        :type redirect_uri: str
        :param access_token: an access_token obtained when the user authorized this integration to access their account
        :type access_token: str
        :param refresh_token: a refresh_token obtained with the initial access_token.
                              Use it to obtain a new access_token
        :type refresh_token: str
        :param account_id: the selected account ID to use with Basecamp 3
        :type account_id: int
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.account_id = account_id

    @property
    def is_usable(self):
        """
        Checks to see if enough fields are present to make API calls. Only checks that the fields have values. No check
        is made to see if the tokens are expired or malformed.

        This will return True if we only have an access_token. This can be misleading because access_tokens eventually
        expire. If the config has no refresh_token, this config will cease to be usable (but you won't know that until
        you actually try to use it).

        :return: True if the API is potentially callable with the information given or False if it lacks required fields
        :rtype: bool
        """
        can_refresh_tokens = self.client_id and self.client_secret and self.redirect_uri and self.refresh_token
        return bool(can_refresh_tokens or self.access_token)

    @abc.abstractmethod
    def read(self):
        """
        Set all of this object's fields to the values found in persistent storage
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self):
        """
        Persist the currently configured fields' values to some sort of storage
        """
        raise NotImplementedError()


class BasecampMemoryConfig(BasecampConfig):
    """
    Store the BasecampConfig fields entirely within memory. read() and save() are no-ops.
    """
    def read(self):
        """
        There is no persistence here. Do nothing.
        """
        return

    def save(self):
        """
        There is no persistence here. Do nothing.
        """
        return


class BasecampFileConfig(BasecampConfig):
    """
    Stores credentials to a .conf file in INI format.
    """
    DEFAULT_CONFIG_FILE_LOCATIONS = [
        "basecamp.conf",  # current directory takes precedence
        constants.DEFAULT_CONFIG_FILE,
        "/etc/basecamp.conf",
    ]
    """A list of places to look for a configuration file if you do not specify one to the Basecamp3 object."""

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, access_token=None, refresh_token=None,
                 account_id=None, filepath=None):
        """
        Create a new BasecampConfig with the given values already set. Bare in mind that the fields for this object
        remain unchanged until you actually call the read() function. This is in case the file doesn't exist yet and
        you are creating the object in order to save() it first.

        :param filepath: the path to read from or save to
        :type filepath: str
        """
        super(BasecampFileConfig, self).__init__(client_id=client_id, client_secret=client_secret,
                                                 redirect_uri=redirect_uri, access_token=access_token,
                                                 refresh_token=refresh_token, account_id=account_id)
        self.filepath = filepath

    def read(self, filepath=None):
        """
        Replace this object's values with those read from a file. If you specify a filepath when calling this function,
        that filepath is used to load values AND it is set as this object's new filepath (for saving or reading from
        later). If you do not specify a filepath, the filepath defined when you created this object is used instead.

        :param filepath: optionally specify a new place to read a filepath
                         from (and set future reads/writes to that file)
        :type filepath: str
        """
        if filepath is None:
            filepath = self.filepath
        config = ConfigParser()
        config.read(filepath)
        attrs = [k for k in self.FIELDS_TO_PERSIST]
        for key in attrs:
            try:
                value = config.get('BASECAMP', key)
                setattr(self, key, value)
            except NoOptionError:
                pass
        self.filepath = filepath  # in case it was specified in the call to read()

    def save(self, filepath=None):
        """
        Save the configuration fields in this object to a file. If you specify a filepath, an INI format configuration
        file will be stored there, and future read/writes will be to that filepath. If you do not specify a filepath,
        the filepath you specified when creating this object will be used.

        :param filepath: optionally choose a new location to save the configuration data to
        :type filepath: str
        """
        if filepath is None:
            filepath = self.filepath
        try:
            os.makedirs(os.path.dirname(filepath), mode=0o770)
        except OSError:
            pass  # folder probably already exists

        config = ConfigParser()
        config.add_section('BASECAMP')
        attrs = [k for k in self.FIELDS_TO_PERSIST]
        for key in attrs:
            try:
                value = getattr(self, key)
                if value is None:
                    continue
                config.set('BASECAMP', key, six.text_type(value))
                setattr(self, key, value)
            except (NoSectionError, NoOptionError):
                pass
        with open(filepath, "w") as fileout:
            config.write(fileout)
        self.filepath = filepath

    @classmethod
    def from_filepath(cls, filepath):
        """
        Create a new configuration object from a given filepath. Equivalent to calling:
            ```py
            config = BasecampFileConfig(filepath=filepath)
            config.read()
            ```
        :param filepath: path to a file to read configuration data from
        :return: a new instance of BasecampFileConfig
        :rtype basecampy3.config.BasecampFileConfig
        """
        if not os.path.exists(filepath):
            raise IOError("Non-existent configuration file '%s'" % filepath)
        new_config = cls()
        new_config.read(filepath)
        return new_config

    @classmethod
    def load_from_default_paths(cls):
        """
        Cycle through a list of default config file locations and attempt to load them in order, stopping when one
        actually works. File not found errors are ignored. Other errors are logged.

        :return: a new instance of BasecampFileConfig
        :rtype basecampy3.config.BasecampFileConfig
        :raises basecampy3.exc.NoDefaultConfigurationFound: if none of the files in the list exist
        """
        env_defined = os.getenv("BC3_CONFIG_PATH")
        if env_defined:
            cls.DEFAULT_CONFIG_FILE_LOCATIONS.insert(0, env_defined)
        for config_file in cls.DEFAULT_CONFIG_FILE_LOCATIONS:
            try:
                return cls.from_filepath(config_file)
            except (IOError, OSError):
                pass  # the file probably does not exist
            except Exception as ex:
                logger.error("%s: %s is invalid.", type(ex).__name__, config_file)
        else:
            raise exc.NoDefaultConfigurationFound()
