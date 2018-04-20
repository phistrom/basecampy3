from __future__ import print_function
import argparse
import errno
import logging
import json
import os
import sys
import traceback
from basecampy3 import Basecamp3, exc
from basecampy3.constants import VERSION
from basecampy3.token_requestor import TokenRequester
from basecampy3.config import BasecampConfig


try:
   input = raw_input  # Python 2
except NameError:  # Python 3
    pass


class CommandLineInvalidError(ValueError):
    pass


class CLI(object):
    """
    A command line interface for Basecamp 3.

    The basics:
      - `$ bc3 configure`
      Walks you through obtaining your Basecamp 3 API credentials. Requires that you create an app first at
      https://launchpad.37signals.com/integrations first
      - `$ bc3 alias add name value`
      Use the alias command to make it easier to execute commands against objects in Basecamp 3 that require an ID.
      While the command line can do some searching to find a Project by its name, Basecamp 3 allows you to make
      multiple Projects with the same name. By aliasing a Project's ID to an easy-to-remember name, you can reference
      Projects simply and avoid ambiguity. Aliases cannot start with a digit and you must prepend a . when referring to
      them in a later command (not for the "add" command).

      For example: `$ bc3 alias add SomeProject 1234567` would allow you to refer to Project ID 1234567 by using
      `bc3 projects get .SomeProject`

      Aliases are, by default, stored in ~/.conf/basecamp_aliases.json but you can change this using
      `--alias-file <some other path>`

      You can also type `bc3 --help` for general usage information, as well as `bc3 projects --help` for more
      usage info at the projects level.
    """

    DEFAULT_ALIAS_FILE_PATH = os.path.expanduser("~/.conf/basecamp_aliases.json")
    
    def __init__(self, pretty_print=True, out=sys.stdout, system_exit=False):
        self._bc3 = None
        self.out = out
        self.parser = self._setup_parser()
        args = self.parser.parse_args()

        loglevel = logging.DEBUG if args.debug else logging.INFO
        logging.getLogger().setLevel(loglevel)
        logging.basicConfig()

        if args.__dict__.get('no_pprint'):
            pretty_print = False
        self.pretty_print = pretty_print

        alias_file = args.__dict__.get('alias_file')
        if not alias_file:
            alias_file = self.DEFAULT_ALIAS_FILE_PATH
        aliases = self._read_alias_file(alias_file)
        aliases = aliases if aliases else {}
        self.alias_file = alias_file
        self.aliases = aliases
        self.args = args

        try:
            func = args.func
        except AttributeError:  # no action chosen by user
            self.parser.print_usage()
            return

        if out is sys.stdout:
            encoding = sys.getdefaultencoding()
        else:
            encoding = "utf-8"

        print(encoding)

        try:
            output = func()  # execute the action chosen by user
            dumps_kwargs = {'obj': output, 'fp': self.out, 'encoding': encoding}
            if pretty_print:
                dumps_kwargs['indent'] = 4
            json.dump(**dumps_kwargs)
        except CommandLineInvalidError as ex:
            logging.error(ex.args[0])
            if system_exit:
                exit(1)
        except exc.Basecamp3Error as ex:
            logging.error(ex)
            exit(2)

    @property
    def bc3(self):
        """
        :return: the instance of the basecamPY3 API we're using
        :rtype: basecampy3.Basecamp3
        """
        if not self._bc3:
            self._bc3 = Basecamp3()
        return self._bc3
    
    def _print(self, *args, **kwargs):
        """
        Replace regular print with a print that we can change the output for.
        """
        kwargs['file'] = self.out
        print(*args, **kwargs)

    def _setup_parser(self):
        """
        argparse setup. Define the tree of commands available to a user from the command line.

        :return: the root ArgumentParser
        :rtype: argparse.ArgumentParser
        """
        parser = argparse.ArgumentParser("bc3", description="BasecamPY3 API Tool")
        parser.add_argument("-v", "--version", action='version', version="BasecamPY3 %s" % VERSION)
        parser.add_argument("--debug", "--verbose", dest="debug", action="store_true",
                            help="Enables more verbose output")
        parser.add_argument("--alias-file", help="Use a non-default location for the alias JSON")
        parser.add_argument("--no-pprint", action="store_true", help="Disable pretty printing JSON output")

        subparsers = parser.add_subparsers(title="subcommands", description="valid subcommands")

        configure = subparsers.add_parser('configure', help="Configure tokens for this account")
        configure.set_defaults(func=self.configure)

        alias = subparsers.add_parser('alias', help="Create aliases for frequently used IDs")

        alias_verbs = alias.add_subparsers(title='verb', description="Valid verbs for 'alias'")
        alias_add = alias_verbs.add_parser("add", help="Add a new alias for an ID")
        alias_add.set_defaults(func=self.alias_add)
        alias_add.add_argument("name", type=self._identifier, help="The identifier of this alias.")
        alias_add.add_argument("value", help="The value of the alias. Usually the ID number of some resource.")
        alias_add.add_argument('-r', '--replace', action='store_true',
                               help="If the identifier already exists, replace its value with this one.")
        alias_del = alias_verbs.add_parser("delete", help="Delete an alias no longer wanted")
        alias_del.set_defaults(func=self.alias_del)
        alias_del.add_argument("name", type=self._identifier, help="Identifier to delete.")

        projects = subparsers.add_parser('projects', help="Create, list, update, and trash projects")
        projects_verbs = projects.add_subparsers(title="verb", description="Valid verbs for 'projects'")
        projects_list = projects_verbs.add_parser("list", help="List projects")
        projects_list.set_defaults(func=self.projects_list)
        projects_list.add_argument('--limit', type=int)
        projects_list.add_argument('--status', help="Valid options are 'archived' or 'trashed' to list only projects "
                                                    "with that status.")
        projects_list.add_argument('--detailed', action="store_true", help="Get all the details of each Project and "
                                                                           "not just the ID and name.")

        projects_get = projects_verbs.add_parser("get", help="Get a project by ID")
        projects_get.set_defaults(func=self.projects_get)
        projects_get.add_argument("id_or_name", help="Get a single Project's information by ID, name, or alias.")
        projects_get.add_argument("--exact", action="store_true", help="if using a name, must match exactly")

        return parser

    def _read_alias_file(self, filepath=None):
        """
        Read in a JSON file containing user-defined aliases for names.

        :param filepath: path to the JSON file. Defaults to the filepath defined at the instance level.
        :type filepath: str
        :return: a dictionary of aliases where the key is the alias identifier, and the value is what the alias
                 resolves to
        :rtype: dict
        """
        if not filepath:
            filepath = self.alias_file
        try:
            with open(filepath, 'r') as infile:
                aliases = json.load(infile)
            return aliases
        except IOError as ex:
            if ex.errno != errno.ENOENT:  # ignore file not found error, raise on anything else though
                raise ex

    def _save_alias_file(self, filepath=None):
        """
        Save aliases back to the JSON file.

        :param filepath: the filepath to the JSON file. Defaults to the instance-defined file path.
        :type filepath: str
        """
        if not filepath:
            filepath = self.alias_file
        self._ensure_dir_exists(filepath)
        with open(filepath, 'w') as outfile:
            json.dump(self.aliases, outfile)

    @staticmethod
    def _ensure_dir_exists(filepath):
        """
        Helper function to just define a path and ignore errors if it exists.

        :param filepath: a full file path. This function makes sure the directories up to the final item exist
        :type filepath: str
        """
        dirname = os.path.dirname(filepath)
        try:
            os.makedirs(dirname, 0o770)
        except OSError as ex:
            if ex.errno != errno.EEXIST:  # only ignore the "File exists" error.
                raise ex

    @staticmethod
    def _identifier(name):
        """
        For use by the argparse alias commands. Ensures that alias identifiers follow the rule that they are not empty
        and do not start with a digit.

        Raises an error if the string was invalid, otherwise just returns the exact same string.

        :param name: the name of the identifier to check
        :type name: str
        :return: the name passed in completely unchanged
        :rtype: str
        """
        try:
            invalid = not name
            invalid = name[0].isdigit()
        except:
            invalid = True
        if invalid:
             raise CommandLineInvalidError("Invalid identifier")
        return name

    def alias_add(self):
        """
        Handles the `bc3 alias add <name> <value>` command.
        Adds a new alias identifier:value pair to the JSON file dictionary.
        """
        args = self.args.__dict__
        name = args['name']
        value = args['value']
        replace = args.get("replace", False)

        if name in self.aliases and not replace:
            ex = CommandLineInvalidError("%s is already defined. Use -r to force replacement." % name)
            raise ex
        self.aliases[name] = value
        self._print("%s = %s" % (name, self.aliases[name]))
        self._save_alias_file()

    def alias_del(self):
        """
        Handles the `bc3 alias delete <name>` command.
        Deletes the given alias from the alias JSON file.
        """
        args = self.args.__dict__
        name = args['name']

        try:
            self.aliases.pop(name)
            self._print("Deleted alias '%s'" % name)
        except KeyError:
            raise CommandLineInvalidError("Couldn't delete %s because it doesn't exist." % name)
        self._save_alias_file()

    def configure(self):
        """
        Handles the `bc3 configure` command.
        A wizard to walk the user through getting their access and refresh tokens. Requires a username and password to
        get the authorization. See token_requestor.py for more information. Saves the necessary information to a
        configuration file the user can pick. Does not store their username or password.
        """
        self._print("This will generate an access token and refresh token for using the Basecamp 3 API.")
        self._print("If you have not done so already, you need to create an app at:")
        self._print("https://launchpad.37signals.com/integrations")

        client_id = input("What is your app's Client ID?").strip()
        client_secret = input("What is your app's Client Secret?").strip()
        redirect_uri = input("What is your app's Redirect URI?").strip()
        self._print("For this next bit we need your username and password. When you have finished this wizard and have "
                    "obtained your access and request tokens, you can change your password as the refresh token is all "
                    "we will need.")
        user_email = input("What is the email address you log into Basecamp with?").strip()
        user_pass = input("What is your password for logging into Basecamp?").strip()
        self._print("Obtaining your access key and refresh token...")
        requestor = TokenRequester(client_id, redirect_uri, user_email, user_pass)
        code = requestor.get_user_code()
        tokens = Basecamp3.trade_user_code_for_access_token(client_id=client_id, redirect_uri=redirect_uri,
                                                            client_secret=client_secret, code=code)
        self._print("Success! Your tokens are listed below.")
        self._print("Access Token: %s" % tokens['access_token'])
        self._print("Refresh Token: %s" % tokens['refresh_token'])
        while True:
            should_save = input("Do you want to save? (Y/N)").upper().strip()
            if should_save in ("Y", "YES"):
                should_save = True
                break
            elif should_save in ("N", "NO"):
                should_save = False
                break
            else:
                self._print("Sorry I don't understand. Please enter Y or N.")
        if should_save is False:
            return
        while True:
            location = input("Where should I save? (default ~/.conf/basecamp.conf)")
            location = location.strip()
            if not location:
                location = os.path.expanduser("~/.conf/basecamp.conf")
            try:
                conf = BasecampConfig(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                      access_token=tokens['access_token'], refresh_token=tokens['refresh_token'])
                conf.save(location)
                break
            except Exception as ex:
                logging.error(traceback.format_exc())
                self._print("Failed to save to '%s'" % location)

    def projects_get(self):
        """
        Handles the `bc3 projects get <id_or_name>` command.
        Pretty print out multiple projects by name, description, or ID number.
        With the --exact flag, only print a single project that:
            - was found in the user's Basecamp 3 account
            - the name of the Project matches exactly (case-insensitive)
            - there are no other Projects with that exact same name (no ambiguity)
            OR
            - the ID was used to get the exact Project (guarantees at most 1 Project returned)
        """
        args = self.args.__dict__
        exact = args.get('exact', False)
        id_or_name = args.get('id_or_name')
        projects = self._get_by_id_or_name(id_or_name, exact=exact)
        if exact:
            projects = [projects]
        return {"projects": [p.all_values for p in projects]}

    def projects_list(self):
        """
        Get a list of Project IDs and names.

        :return:
        """
        args = self.args.__dict__
        status = args.get('status', None)
        limit = args.get('limit', None)
        detailed = args.get('detailed')
        projects = []
        for idx, project in enumerate(self.bc3.projects.list(status=status), start=1):
            if detailed:
                projects.append(project.all_values)
            else:
                projects.append(project.summary_values)
            if limit and idx >= limit:
                break
        return {"projects": projects}

    def _resolve_alias(self, alias_name):
        try:
            return self.aliases[alias_name]
        except KeyError:
            raise CommandLineInvalidError("Unknown alias .%s" % alias_name)

    def _get_by_id_or_name(self, id_or_term, exact=False):
        if id_or_term.startswith("."):  # this must be an alias
            alias_name = id_or_term[1:]  # get the rest of the name after the "."
            id_or_term = self._resolve_alias(alias_name)  # look up the alias in the table
        try:
            if id_or_term.isdigit():  # assume this is a project's ID
                project = self.bc3.projects.get(id_or_term)
                if exact:
                    return project
                else:
                    return [project]
        except exc.Basecamp3Error:
            pass  # ok maybe there's a project with a number for its name instead?

        if exact:
            find_kwargs = {"name": id_or_term}  # search the name only
        else:
            find_kwargs = {"any": id_or_term}  # search description AND name
        projects = self.bc3.projects.find(**find_kwargs)

        if not projects:  # no results at all!
            ex = CommandLineInvalidError("No projects found that matched '%s'" % id_or_term)
            raise ex

        if exact:
            if len(projects) > 1:  # too many results!
                ex = CommandLineInvalidError("Found %s projects that match '%s': %s" %
                                             (len(projects), id_or_term, "', '".join([p.name for p in projects])))
                raise ex
            if projects[0].name.upper() != id_or_term.upper():
                ex = CommandLineInvalidError("Did not find an exact match for '%s'. Did you mean '%s'?." %
                                             (id_or_term, projects[0].name))
                raise ex
            return projects[0]  # return the one result object
        else:
            return projects  # return results as a list


def main():
    CLI(system_exit=True)


if __name__ == "__main__":
    main()
