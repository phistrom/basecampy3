#!/usr/bin/env python
"""
This module is responsible for the "bc3" command line tool functionality.
"""
import argparse
import logging
import os
import traceback

from basecampy3 import Basecamp3, exc
from basecampy3.bc3_api import _create_session
from basecampy3.token_requestor import TokenRequester
from basecampy3 import config, constants

try:
    # noinspection PyShadowingBuiltins
    input = raw_input  # Python 2
except NameError:  # Python 3
    pass


class CLI(object):
    @classmethod
    def from_command_line(cls):
        """
        Assemble an ArgumentParser to accept command line parameters.
        """
        new = cls()
        parser = argparse.ArgumentParser("bc3", description="BasecamPY3 API Tool")
        parser.add_argument("--debug", "--verbose", dest="debug", action="store_true",
                            help="Enables more verbose output")
        # parser.add_argument('command', help="The section of the API to access.")
        subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands")
        configure = subparsers.add_parser('configure', help="Configure tokens for this account")
        configure.set_defaults(func=cls._configure)
        # projects = subparsers.add_parser("projects", help="Manipulate project data in Basecamp")
        version = subparsers.add_parser("version", help="Displays the installed version of BasecamPY3")
        version.set_defaults(func=cls._version)
        args = parser.parse_args()
        loglevel = logging.DEBUG if args.debug else logging.INFO
        logging.getLogger().setLevel(loglevel)
        logging.basicConfig()
        try:
            args.func()
        except AttributeError:
            parser.print_usage()
            return

        return new

    @staticmethod
    def _configure():
        """
        An interactive wizard to walk a user through authorizing a Basecamp 3 API integration and storing the
        resulting tokens in basecamp.conf
        """
        print("This will generate an access token and refresh token for using the Basecamp 3 API.")
        print("You must first create your own integration if you have not already here:")
        print("See the NOTE below about 'Redirect URI', otherwise give your integration any name and website you wish.")
        print("https://launchpad.37signals.com/integrations")
        print("This wizard will attempt to open your web browser to Basecamp's website where you will sign in and \n"
              "allow your own Basecamp integration access to your own Basecamp account.")
        print("NOTE: If you are running bc3 configure via SSH or a headless system of some kind, you should stop, \n"
              "run bc3 configure on a different system with a functional web browser, and then transplant the \n"
              "resulting basecamp.conf file to this system.")
        print("NOTE: The 'Redirect URI' you specify on your integration page MUST match the default \n"
              "'http://localhost:33333' OR a URL you specify on step 3. The only reason to change this is if TCP \n"
              "port 33333 is already in use or blocked on your computer. A local HTTP server is started to listen \n"
              "for the authorization code redirect. If you specify a non-localhost or fictitious address, the code \n"
              "will not be picked up by this wizard and you will have to cancel and retry using CTRL+C.")
        print("\n")
        client_id = input("What is your app's Client ID? ").strip()
        client_secret = input("What is your app's Client Secret? ").strip()
        redirect_uri = input("What is your redirect URI? (Press enter to use the stongly recommended default '%s') " %
                             constants.DEFAULT_REDIRECT_URI)

        if not (client_id and client_secret):
            raise RuntimeError("No client ID or secret provided. Cannot continue.")

        if not redirect_uri:
            redirect_uri = constants.DEFAULT_REDIRECT_URI

        print("Obtaining your access key and refresh token...")
        session = _create_session()
        requester = TokenRequester(client_id, redirect_uri, session)
        code = requester.get_authorization()
        tokens = Basecamp3.trade_user_code_for_access_token(client_id, redirect_uri, client_secret, code, session)
        print("Success! Your tokens are listed below.")
        print("Access Token: %s" % tokens['access_token'])
        print("Refresh Token: %s" % tokens['refresh_token'])
        bc3api = Basecamp3(access_token=tokens['access_token'])
        identity = bc3api.who_am_i["identity"]
        accounts = [acct for acct in bc3api.accounts]
        if len(accounts) < 1:
            print("Error: You don't seem to have any Basecamp accounts")
            raise exc.UnknownAccountIDError()
        elif len(accounts) == 1:
            account_id = accounts[0]["id"]
        else:
            while True:
                print("User ID %s, email %s has %s accounts. Which one do you want to use?" %
                      (identity["id"], identity["email_address"], len(accounts)))
                for idx, acct in enumerate(accounts, start=1):
                    print("%s) %s (ID = %s)" % (idx, acct["name"], acct["id"]))
                choice = input("Which of the above accounts do you want to use? ")
                try:
                    choice = abs(int(choice))
                    acct = accounts[choice - 1]
                    account_id = acct["id"]
                    print("Selected %(name)s (ID = %(id)s)" % acct)
                    break
                except (IndexError, TypeError, ValueError):
                    print("%s is not a valid choice. Please provide a number between 1 and %s" %
                          (choice, len(accounts)))

        while True:
            should_save = input("Do you want to save? (Y/N)").upper().strip()
            if should_save in ("Y", "YES"):
                should_save = True
                break
            elif should_save in ("N", "NO"):
                should_save = False
                break
            else:
                print("Sorry I don't understand. Please enter Y or N.")
        if should_save is False:
            return
        while True:
            location = None
            if os.getenv("BC3_CONTAINER") != "1":  # don't prompt user for location in a container
                location = input("Where should I save? (default %s)" % constants.DEFAULT_CONFIG_FILE)
                location = location.strip()
            if not location:  # we're in a container or no response from user so use the default
                location = constants.DEFAULT_CONFIG_FILE
            try:
                conf = config.BasecampFileConfig(client_id=client_id, client_secret=client_secret,
                                                 redirect_uri=redirect_uri, access_token=tokens['access_token'],
                                                 refresh_token=tokens['refresh_token'], account_id=account_id)
                conf.save(location)
                break
            except Exception:
                logging.error(traceback.format_exc())
                print("Failed to save to '%s'" % location)

    @staticmethod
    def _version():
        print("BasecamPY3 %s" % constants.VERSION)

    # @staticmethod
    # def _get_modules():
    #     # find all endpoint modules
    #     endpoint_modules = inspect.getmembers(basecampy3.endpoints, inspect.ismodule)
    #     modules = []
    #     endpoint_map = {}
    #     for module_name, module in endpoint_modules:
    #         if module_name in ('_base', 'util'):  # exclude non-endpoint modules
    #             continue
    #         endpoint_dict = {}
    #
    #         classes = inspect.getmembers(module, inspect.isclass)
    #         for classname, cls in classes:
    #             # find the class for this Endpoint
    #             if cls is not BasecampEndpoint and issubclass(cls, BasecampEndpoint):
    #                 # this is our Endpoint, get its non-private methods
    #                 methods_dict = {mthd[0]: mthd for mthd in inspect.getmembers(cls, inspect.ismethod)
    #                                 if not mthd[0].startswith('_')}
    #
    #                 endpoint_dict[classname] = methods_dict
    #
    #                 endpoint_map[module_name] = endpoint_map
    #                 break
    #
    #         issubclass(inspect.getmembers(module, inspect.isclass)[3][1], basecampy3.endpoints._base.BasecampEndpoint)
    #     return {m[0]: m[1] for m in endpoint_modules if m[0] not in ("_base", "util")}


def main():
    """
    Entrypoint for the bc3 console script installed by `pip install basecampy3`.
    """
    CLI.from_command_line()
    exit(0)


if __name__ == "__main__":
    main()
