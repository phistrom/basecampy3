import unittest
import uuid
from basecampy3 import Basecamp3, config, constants
from datetime import datetime
import logging


class APITest(unittest.TestCase):
    PROJECT_TEST_NAME_PREFIX = "_DELETE_pytest__basecampy3_"
    PROJECT_TEST_DESCRIPTION = "Trash me I am a test project."

    def setUp(self):
        self.api = Basecamp3()

    def tearDown(self):
        # trash any projects we missed
        trashed = 0
        for project in self.api.projects.list():
            if project.name.startswith(self.PROJECT_TEST_NAME_PREFIX):
                logging.info("Sending project '%s' to trash." % project.name)
                project.trash()
                trashed += 1
        logging.info("Test(s) complete. Deleted %s test project(s)." % trashed)

    def test_direct_parameters(self):
        conf = config.BasecampFileConfig.from_filepath(constants.DEFAULT_CONFIG_FILE)
        parameters = {k: getattr(conf, k) for k in config.BasecampConfig.FIELDS_TO_PERSIST}

        # first we'll try with a custom BasecampConfig object passed into the Basecamp3 constructor
        custom_config = config.BasecampMemoryConfig(**parameters)
        bc3a = Basecamp3(conf=custom_config)
        p = None
        for p in bc3a.projects.list():
            break
        assert p is not None

        # next we'll pass the parameters directly into the Basecamp3 constructor
        bc3b = Basecamp3(**parameters)
        p = None
        for p in bc3b.projects.list():
            break
        assert p is not None

        # next we'll try with just an access_token and nothing else
        bc3c = Basecamp3(access_token=conf.access_token)
        p = None
        for p in bc3c.projects.list():
            break
        assert p is not None

    def test_projects(self):
        """
        Create 3 projects with random names, ensure they show up in the list of projects, delete them.
        """
        project_names = {}
        for _ in range(0, 3):
            key = "%s%s" % (self.PROJECT_TEST_NAME_PREFIX, uuid.uuid4())
            project_names[key] = None

        for name in project_names:
            new_project = self.api.projects.create(name, description=self.PROJECT_TEST_DESCRIPTION)
            assert new_project.name == name
            assert new_project.description == self.PROJECT_TEST_DESCRIPTION
            project_names[name] = new_project.id

        projects_found = {name: False for name in project_names}

        for project in self.api.projects.list():
            if project.name in project_names and project.id == project_names[project.name]:
                projects_found[project.name] = True
                project.trash()

        for found in projects_found.values():
            assert found

        for project_id in project_names.values():
            project = self.api.projects.get(project_id)
            assert project.status == "trashed"

        logging.info("test_projects complete :)")

    def test_campfire(self):
        project_name = "%sCampfire" % self.PROJECT_TEST_NAME_PREFIX
        campfire_test_message = "I'm a robot beep boop '%s'" % uuid.uuid4()
        project = self.api.projects.create(project_name)
        project.campfire.post_message(campfire_test_message)

        expected_count = 1
        for counter, line in enumerate(project.campfire.lines):
            assert counter < expected_count
            assert line.content == campfire_test_message

        logging.info("test_campfire complete :)")

    def test_message_board(self):
        project_name = "%sMessageBoard" % self.PROJECT_TEST_NAME_PREFIX
        empty_test_subject = "This message has no body"
        test_subject = "This is a test message"
        test_content = ""
        project = self.api.projects.create(project_name)
        message_types = [t for t in project.message_board.message_types]
        empty_body = project.message_board.post_message(empty_test_subject, content=None)
        test_msg = project.message_board.post_message(test_subject, test_content, category=message_types[1])

        expected_count = 2
        for counter, message in enumerate(project.message_board.list()):
            assert counter < expected_count
            if message.id == test_msg.id:
                assert message.subject == test_subject
                assert test_content in message.content
                message.trash()
            elif message.id == empty_body.id:
                assert message.subject == empty_test_subject
                assert message.content == ""
                message.trash()

        logging.info("test_message_board complete :)")

    def test_todos(self):
        project_name = "%sTODOs" % self.PROJECT_TEST_NAME_PREFIX
        todolist_name = "A Nice Little Todo List"
        todoitem_name1 = "First I have to do this"
        todoitem_name2 = "Then I do that"
        todoitem_name3 = "but actually I will do this first"
        todogroup_name1 = "Awesome"
        todogroup_name2 = "Not awesome"
        project = self.api.projects.create(project_name)
        test_list = project.todoset.create(todolist_name)

        expected_count = 1
        for counter, todolist in enumerate(project.todoset.list()):
            assert counter < expected_count
            if todolist.id == test_list.id:
                assert todolist.name == todolist_name

        todoitem1 = test_list.create(content=todoitem_name1)
        todoitem2 = test_list.create(content=todoitem_name2)
        todoitem3 = test_list.create(content=todoitem_name3)
        todogroup1 = test_list.create_group(name=todogroup_name1)
        todogroup2 = test_list.create_group(name=todogroup_name2)
        todoitem3.reposition(1)
        todogroup1.reposition(5)

        items = [todoitem3, todoitem1, todoitem2]  # order in which these items should be now

        for counter, todoitem in enumerate(test_list.list()):
            assert todoitem.id == items[counter].id
            assert todoitem.content == items[counter].content

        todogroups = [todogroup2, todogroup1]  # order in which these TodoListGroups should appear
        for counter, todogroup in enumerate(test_list.list_groups()):
            assert todogroup.id == todogroups[counter].id
            assert todogroup.name == todogroups[counter].name

        todoitem3.check()

        expected = 1
        for counter, todoitem in enumerate(test_list.list(completed=True)):
            assert counter < expected
            assert todoitem.id == todoitem3.id

        items.pop(0)
        for counter, todoitem in enumerate(test_list.list()):
            assert todoitem.id == items[counter].id

        todoitem1.trash()

        todoitem1.refresh()

        assert todoitem1.status == "trashed"
        logging.info("test_todos complete :)")

    def _create_test_project(self, middle="", suffix=None):
        if suffix is None:
            suffix = uuid.uuid4()
        name = "%s%s%s" % (self.PROJECT_TEST_NAME_PREFIX, middle, suffix)
        project = self.api.projects.create(name, description=self.PROJECT_TEST_DESCRIPTION)
        return project
