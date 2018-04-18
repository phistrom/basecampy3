"""
A configuration object used by the API object. Looks for a basecamp.conf file at startup and makes it a variable
called GLOBAL. If nothing is specified when you make a Basecamp API object, the GLOBAL configuration will be used.

Reads from INI files. Also writes back to the INI files if you use this API to obtain access or refresh tokens.
"""
try:
    from ConfigParser import SafeConfigParser as ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoSectionError, NoOptionError

from datetime import datetime, timedelta
import logging
import os
import six

from .exc import *


class BasecampConfig(object):
    DEFAULT_CONFIG_FILE_LOCATIONS = [
        "basecamp.conf",  # current directory
        os.path.expanduser("~/.conf/basecamp.conf"),  # user profile directory/.conf/basecamp.conf
        "/etc/basecamp.conf",
    ]

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, user_email=None, user_pass=None,
                 access_token=None, access_expires=None, refresh_token=None, filepath=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.user_email = user_email
        self.user_pass = user_pass
        self.access_token = access_token
        self._access_expires = datetime.min
        if access_expires is not None:
            self.access_expires = access_expires
        self.refresh_token = refresh_token
        self.filepath = filepath

    @property
    def access_expires(self):
        return self._access_expires

    @access_expires.setter
    def access_expires(self, value):
        if isinstance(value, datetime):
            self._access_expires = value
            return

        try:
            value = float(value)
            value = datetime.now() + timedelta(seconds=value)
        except:
            raise ValueError("`access_expires` needs to be a float (number of seconds until expiration) "
                             "or a datetime. Got a `%s`." % type(value).__name__)
        self._access_expires = value

    def read(self, filepath):
        config = ConfigParser()
        config.read(filepath)
        attrs = [k for k in self.__dict__.keys() if k not in ('filepath', '_access_expires')]
        attrs.append('access_expires')
        for key in attrs:
            try:
                value = config.get('BASECAMP', key)
                if key == "access_expires":
                    value = datetime.utcfromtimestamp(float(value))
                setattr(self, key, value)
            except NoOptionError:
                pass
        self.filepath = filepath

    def save(self, filepath=None):
        if filepath is None:
            filepath = self.filepath
        try:
            os.makedirs(os.path.dirname(filepath), mode=0o770)
        except OSError:
            pass  # folder probably already exists

        config = ConfigParser()
        config.add_section('BASECAMP')
        attrs = [k for k in self.__dict__.keys() if k != 'filepath']
        for key in attrs:
            try:
                value = getattr(self, key)
                if value is None:
                    continue
                if key == "_access_expires":
                    key = "access_expires"
                    try:
                        value = value.timestamp()
                    except:
                        continue  # if timestamp is at min value, this will fail, that's ok

                config.set('BASECAMP', key, six.text_type(value))
                setattr(self, key, value)
            except (NoSectionError, NoOptionError):
                pass
        with open(filepath, "w") as fileout:
            config.write(fileout)
        self.filepath = filepath

    @classmethod
    def from_filepath(cls, filepath):
        if not os.path.exists(filepath):
            raise IOError("Non-existent configuration file '%s'" % filepath)
        new_config = cls()
        new_config.read(filepath)
        return new_config

    @classmethod
    def load_from_default_paths(cls):
        for config_file in cls.DEFAULT_CONFIG_FILE_LOCATIONS:
            try:
                return cls.from_filepath(config_file)
            except Exception as ex:
                logging.debug("%s: %s is missing or invalid.", type(ex).__name__, config_file)
        else:
            raise NoDefaultConfigurationFound()
