# -*- coding: utf-8 -*-
"""
Tests for the basecampy3.urls package.
"""

from __future__ import unicode_literals

import logging
import os
import re
import time
import unittest
import uuid
from datetime import date, datetime, timedelta

import dateutil
import pytz
from tzlocal import get_localzone

from basecampy3 import Basecamp3, exc

logger = logging.getLogger("basecampy3")
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logging.getLogger("basecampy3.transport_adapter").setLevel(logging.INFO)

try:
    PRE_MADE_PROJECT_ID = os.environ["BC3_TEST_PROJECT_ID"]
    """
    REQUIRED: An ID for a Project you create in advance that must have 
    a Question (Check-In), an Answer to that Question, and Email Forwards
    must be enabled.
    """
except Exception:
    raise EnvironmentError("You must define environment variable "
                           "'BC3_TEST_PROJECT_ID' so that Questions and "
                           "Forwards can be tested.")


class APITest(unittest.TestCase):
    PROJECT_TEST_NAME_PREFIX = "_DELETE_pytest__basecampy3_"
    PROJECT_TEST_DESCRIPTION = "Trash me I am a test project."
    UPLOAD_TEST_FILE_NAME = "testfile.png"
    api = None

    def __init__(self, methodName='runTest'):
        super(APITest, self).__init__(methodName=methodName)
        if APITest.api is None:
            APITest.api = Basecamp3()

    def setUp(self):
        proj = self._create_test_project(middle="URLs")
        self.project_id = proj["id"]
        dock = proj["dock"]
        dock_by_name = {i["name"]: i["id"] for i in dock}
        self.campfire_id = dock_by_name["chat"]
        self.message_board_id = dock_by_name["message_board"]
        self.todoset_id = dock_by_name["todoset"]
        self.schedule_id = dock_by_name["schedule"]
        self.questionnaire_id = dock_by_name["questionnaire"]
        self.vault_id = dock_by_name["vault"]
        self.inbox_id = dock_by_name["inbox"]

        # premade project that will be used for
        # a subset of the tests (because they do not support
        # creation via the API, the data must already exist)
        url = self.api.urls.projects.get(project=PRE_MADE_PROJECT_ID)
        data = self._get_data(url)
        self.premade_project = data["id"]
        dock = data["dock"]
        dock_by_name = {i["name"]: i["id"] for i in dock}
        self.premade_questionnaire = dock_by_name["questionnaire"]
        self.premade_inbox = dock_by_name["inbox"]

    def tearDown(self):
        # trash any projects we missed
        trashed = 0
        url = self.api.urls.projects.list()
        response = url.request(self.api.session)
        if not response.ok:
            logger.error("Unable to list projects to delete test projects.")
            raise exc.Basecamp3Error(response=response)
        data = response.json()
        projects_to_delete = [pd for pd in data if pd["name"].startswith(self.PROJECT_TEST_NAME_PREFIX)]
        errors = []
        for project in projects_to_delete:
            del_url = self.api.urls.projects.trash(project["id"])
            response = del_url.request(self.api.session)
            if not response.ok:
                ex = exc.Basecamp3Error(response=response)
                errors.append(ex)
            else:
                trashed += 1
        if errors:
            for error in errors:
                logger.error(error)
            logger.error("Not all test projects got deleted.")
        logger.info("Test(s) complete. Deleted %s out of %s test project(s).",
                    trashed, len(projects_to_delete))
        time.sleep(1)

    def _create_test_project(self, middle="", suffix=None):
        if suffix is None:
            suffix = uuid.uuid4()
        name = "%s%s%s" % (self.PROJECT_TEST_NAME_PREFIX, middle, suffix)
        url = self.api.urls.projects.create(name=name, description=self.PROJECT_TEST_DESCRIPTION)
        response = url.request(self.api.session)
        if not response.ok:
            logger.error("Unable to create a test project.")
            raise exc.Basecamp3Error(response=response)
        project_data = response.json()
        return project_data

    def test_campfire_lines(self):
        test_text = "Good morning!"

        # Create Campfire Line
        data = self._create_campfire_line(test_text)
        line_id = data["id"]
        assert data["content"] == test_text

        # Get Campfire Line
        data = self._get_campfire_line(line_id)
        assert data["id"] == line_id
        assert data["content"] == test_text

        # Get Campfire Line (test caching)
        data = self._get_campfire_line(line_id)
        assert data["id"] == line_id
        assert data["content"] == test_text

        # List Campfire Lines
        data = self._list_campfire_lines()
        assert len(data) == 1

        # Delete the Campfire Line
        url = self.api.urls.campfire_lines.delete(project=self.project_id,
                                                  campfire=self.campfire_id,
                                                  line=line_id)
        self._get_no_content(url)
        logger.info("Successfully tested Campfire Lines!")

    def test_campfires(self):
        # Get Campfire
        url = self.api.urls.campfires.get(project=self.project_id, campfire=self.campfire_id)
        data = self._get_data(url)
        assert data["id"] == self.campfire_id
        assert data["type"] == "Chat::Transcript"
        assert "lines_url" in data

        # List Campfires visible to user account-wide
        url = self.api.urls.campfires.list()
        data = self._get_data(url)
        assert len(data) > 0
        assert data[0]["type"] == "Chat::Transcript"
        assert "lines_url" in data[0]

        logger.info("Successfully tested Campfires!")

    def test_chatbots(self):
        test_service_name = "TestBot%s" % int(time.time())
        test_command_url = "https://example.com"
        test_content = "<strong>Howdy</strong> there."
        # Create Chatbot
        url = self.api.urls.chatbots.create(project=self.project_id,
                                            campfire=self.campfire_id,
                                            service_name=test_service_name,
                                            command_url=test_command_url)
        data = self._get_data(url)
        chatbot_id = data["id"]

        # Get Chatbot
        url = self.api.urls.chatbots.get(project=self.project_id, campfire=self.campfire_id, chatbot=chatbot_id)
        data = self._get_data(url)
        assert data["id"] == chatbot_id
        assert data["service_name"] == test_service_name
        assert data["command_url"] == test_command_url

        # Create Line as Chatbot
        match = re.search(r"integrations/([^/]+)/buckets", data["lines_url"])
        chatbot_key = match.group(1)
        url = self.api.urls.chatbots.create_line(project=self.project_id,
                                                 campfire=self.campfire_id,
                                                 chatbot_key=chatbot_key,
                                                 content=test_content)
        self._get_no_content(url)

        # List Chatbots
        url = self.api.urls.chatbots.list(project=self.project_id, campfire=self.campfire_id)
        data = self._get_data(url)
        assert len(data) > 0

        test_updated_service_name = "two%s" % test_service_name
        test_updated_command_url = "%s/updated" % test_command_url

        # Update Chatbot
        url = self.api.urls.chatbots.update(project=self.project_id,
                                            campfire=self.campfire_id,
                                            chatbot=chatbot_id,
                                            service_name=test_updated_service_name,
                                            command_url=test_updated_command_url)
        data = self._get_data(url)
        assert data["id"] == chatbot_id
        assert data["service_name"] == test_updated_service_name
        assert data["command_url"] == test_updated_command_url

        # Delete Chatbot
        url = self.api.urls.chatbots.delete(project=self.project_id,
                                            campfire=self.campfire_id,
                                            chatbot=chatbot_id)
        self._get_no_content(url)
        logger.info("Successfully tested chatbots!")

    def test_comments(self):
        comment_content = "Just a test comment here."

        # Create Document to put Comments on
        url = self.api.urls.documents.create(project=self.project_id, vault=self.vault_id,
                                             title="Test Comment Document",
                                             content="Does not really matter what is in here...",
                                             status="active")
        data = self._get_data(url)
        document_id = data["id"]

        url = self.api.urls.comments.create(project=self.project_id,
                                            recording=document_id,
                                            content=comment_content)
        data = self._get_data(url)
        comment_id = data["id"]
        assert data["content"] == comment_content

        # Get Comment
        url = self.api.urls.comments.get(project=self.project_id, comment=comment_id)
        data = self._get_data(url)
        assert data["id"] == comment_id
        assert data["content"] == comment_content

        # List Comments by Recording
        url = self.api.urls.comments.list_by_recording(project=self.project_id,
                                                       recording=document_id)
        data = self._get_data(url)
        assert len(data) > 0

        new_comment_content = "I changed my mind."

        # Update Comment
        url = self.api.urls.comments.update(project=self.project_id,
                                            comment=comment_id,
                                            content=new_comment_content)
        data = self._get_data(url)
        assert data["id"] == comment_id
        assert data["content"] == new_comment_content

        self._recording_tests(comment_id, self.api.urls.comments, test_visibility=False)

        # Delete our test document
        self.api.urls.documents.trash(project=self.project_id, recording=document_id)
        logger.info("Successfully tested Comments!")

    def test_documents(self):
        test_title = "Test Document"
        test_content = "I am an awesome <strong>Document!</strong>"

        # Create Document
        url = self.api.urls.documents.create(project=self.project_id, vault=self.vault_id,
                                             title=test_title,
                                             content=test_content,
                                             status="active")
        data = self._get_data(url)
        document_id = data["id"]
        assert data["status"] == "active"
        assert data["title"] == test_title
        assert data["content"] == test_content

        # Get Document
        url = self.api.urls.documents.get(project=self.project_id, document=document_id)
        data = self._get_data(url)
        assert data["id"] == document_id
        print(data)

        # List Documents By Vault
        url = self.api.urls.documents.list_by_vault(project=self.project_id, vault=self.vault_id)
        data = self._get_data(url)
        assert len(data) > 0

        new_document_title = "Oh that is new"
        new_content = "Wowee!<br><br>I am a document!"

        # Update Document
        url = self.api.urls.documents.update(project=self.project_id, document=document_id,
                                             title=new_document_title, content=new_content)

        data = self._get_data(url)
        assert data["id"] == document_id
        assert data["title"] == new_document_title
        assert data["content"] == new_content
        print(data)

        self._recording_tests(document_id, self.api.urls.documents)

        logger.info("Successfully tested Documents!")

    def test_message_boards(self):
        url = self.api.urls.message_boards.get(project=self.project_id,
                                               board=self.message_board_id)
        data = self._get_data(url)
        assert data["id"] == self.message_board_id
        logger.info("Successfully tested Message Boards!")

    def test_message_types(self):
        message_type_name = "Neigh"
        message_type_icon = "🐴"

        # Create new Message Type
        url = self.api.urls.message_types.create(project=self.project_id,
                                                 name=message_type_name,
                                                 icon=message_type_icon)
        data = self._get_data(url)
        message_type_id = data["id"]
        assert message_type_name == data["name"]
        assert message_type_icon == data["icon"]

        # List Message Types
        url = self.api.urls.message_types.list(project=self.project_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get Message Type
        url = self.api.urls.message_types.get(project=self.project_id,
                                              message_type=message_type_id)
        data = self._get_data(url)
        assert data["id"] == message_type_id
        assert message_type_name == data["name"]
        assert message_type_icon == data["icon"]

        new_name = "Moo"
        new_icon = "🐄"

        # Update Message Type
        url = self.api.urls.message_types.update(project=self.project_id,
                                                 message_type=message_type_id,
                                                 name=new_name,
                                                 icon=new_icon)
        data = self._get_data(url)
        assert data["name"] == new_name
        assert data["icon"] == new_icon

        url = self.api.urls.message_types.delete(project=self.project_id,
                                                 message_type=message_type_id)
        self._get_no_content(url)

        logger.info("Successfully tested Message Types!")

    def test_messages(self):
        subject = "BasecamPY Test Subject"
        content = "<strong>Welcome to BasecamPY!</strong><br>Enjoy!"

        # List Message Types
        url = self.api.urls.message_types.list(project=self.project_id)
        data = self._get_data(url)
        # just get the first category to start with
        category_id = data[0]["id"]

        # we'll use this one to test updating later
        new_category_id = data[1]["id"]

        # Create new Message
        url = self.api.urls.messages.create(project=self.project_id,
                                            message_board=self.message_board_id,
                                            subject=subject, content=content,
                                            category_id=category_id)
        data = self._get_data(url)
        message_id = data["id"]
        assert data["subject"] == subject
        assert data["content"] == content

        # List by Message Board
        url = self.api.urls.messages.list_by_message_board(project=self.project_id,
                                                           message_board=self.message_board_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get a Message
        url = self.api.urls.messages.get(project=self.project_id, message=message_id)
        data = self._get_data(url)
        assert data["id"] == message_id
        assert data["category"]["id"] == category_id
        assert data["subject"] == subject
        assert data["content"] == content

        new_subject = "Basecampy3 is neat"
        new_content = "I think so anyway"

        # Update a Message
        url = self.api.urls.messages.update(project=self.project_id,
                                            message=message_id,
                                            subject=new_subject,
                                            content=new_content,
                                            category_id=new_category_id)
        data = self._get_data(url)
        assert data["id"] == message_id
        assert data["category"]["id"] == new_category_id
        assert data["subject"] == new_subject
        assert data["content"] == new_content

        self._recording_tests(message_id, self.api.urls.messages)

        logger.info("Successfully tested Message objects!")

    def test_people(self):
        # Get Current User
        person_id = self._get_current_user()

        # Get User
        url = self.api.urls.people.get(person=person_id)
        data = self._get_data(url)
        assert data["id"] == person_id

        # List Pingable
        url = self.api.urls.people.list_pingable()
        _ = self._get_data(url)

        # List by Project
        url = self.api.urls.people.list_by_project(self.project_id)
        data = self._get_data(url)
        assert len(data) > 0

        # List all People
        url = self.api.urls.people.list()
        data = self._get_data(url)
        assert len(data) > 0

        logger.info("Successfully tested People objects!")

    def test_projects(self):
        # List Projects
        url = self.api.urls.projects.list()
        data = self._get_data(url)
        assert len(data) > 1

        # Get Project
        url = self.api.urls.projects.get(project=self.project_id)
        data = self._get_data(url)
        assert data["id"] == self.project_id
        old_name = data["name"]
        old_desc = data["description"]

        # we will skip Create projects because it gets tested by every other test!

        # Update Project
        new_name = "%s Renamed" % old_name
        new_desc = "%s Modified" % old_desc

        url = self.api.urls.projects.update(project=self.project_id,
                                            name=new_name,
                                            description=new_desc)
        data = self._get_data(url)
        assert data["id"] == self.project_id
        assert data["name"] == new_name
        assert data["description"] == new_desc

        # We will skip trashing a project because that is tested by
        # every other test.

        # Update Membership
        # TODO

        logger.info("Successfully tested Project objects!")

    def test_questionnaires(self):
        # Get Questionnaire
        url = self.api.urls.questionnaires.get(project=self.project_id,
                                               questionnaire=self.questionnaire_id)
        data = self._get_data(url)
        assert data["id"] == self.questionnaire_id

        logger.info("Successfully tested Questionnaire objects!")

    def test_questions_and_answers(self):
        # List Questions
        url = self.api.urls.questions.list(
            project=self.premade_project, questionnaire=self.premade_questionnaire
        )
        data = self._get_data(url)
        question_id = data[0]["id"]

        # Get Question

        url = self.api.urls.questions.get(project=self.premade_project,
                                          question=question_id)
        data = self._get_data(url)
        assert data["id"] == question_id

        # List Answers by Question
        url = self.api.urls.question_answers.list_by_question(
            project=self.premade_project, question=question_id
        )
        data = self._get_data(url)
        answer_id = data[0]["id"]

        # Get Answer by ID
        url = self.api.urls.question_answers.get(
            project=self.premade_project, answer=answer_id
        )
        data = self._get_data(url)
        assert data["id"] == answer_id

        # Test all Recording features of an Answer object
        self._recording_tests(answer_id, self.api.urls.question_answers,
                              test_archiving=False, test_visibility=False,
                              test_events=False, test_subscriptions=False,
                              trash=False)

    def test_schedule_entries(self):
        # purposely use naive, non-UTC datetimes for testing
        now = datetime.now()
        tomorrow = now + timedelta(days=1)

        test_summary = "Basecampy Test Entry"
        test_description = "Attend this test entry <strong>tomorrow!</strong>"

        # Create Schedule Entry
        url = self.api.urls.schedule_entries.create(project=self.project_id,
                                                    schedule=self.schedule_id,
                                                    summary=test_summary,
                                                    starts_at=now,
                                                    ends_at=tomorrow,
                                                    description=test_description,
                                                    all_day=False,
                                                    notify=True)
        data = self._get_data(url)

        # parse the returned dates and set to UTC
        starts_at = dateutil.parser.isoparse(data["starts_at"])
        ends_at = dateutil.parser.isoparse(data["ends_at"])
        starts_at = starts_at.astimezone(pytz.utc)
        ends_at = ends_at.astimezone(pytz.utc)

        # convert original input to UTC
        tz_local = get_localzone()
        now_utc = tz_local.localize(now).astimezone(pytz.utc)
        tomorrow_utc = tz_local.localize(tomorrow).astimezone(pytz.utc)

        # remove the microsecond precision from the original input
        # as it is not preserved in Schedule Entry objects
        now_utc = now_utc.replace(microsecond=0)
        tomorrow_utc = tomorrow_utc.replace(microsecond=0)

        assert starts_at == now_utc
        assert ends_at == tomorrow_utc

        entry_id = data["id"]

        # Get Schedule Entry
        url = self.api.urls.schedule_entries.get(project=self.project_id,
                                                 entry=entry_id)
        data = self._get_data(url)
        assert entry_id == data["id"]

        # List Schedule Entries by Schedule
        url = self.api.urls.schedule_entries.list_by_schedule(project=self.project_id,
                                                              schedule=self.schedule_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Update Schedule Entry
        new_summary = "Basecampy modified summary"
        new_starts_at = datetime.now()
        new_ends_at = new_starts_at + timedelta(hours=1)
        new_desc = "Updated Basecampy description on a scheduled event!"

        url = self.api.urls.schedule_entries.update(
            project=self.project_id, entry=entry_id, summary=new_summary,
            starts_at=new_starts_at, ends_at=new_ends_at, description=new_desc,
            all_day=True, notify=False
        )
        data = self._get_data(url)
        assert data["id"] == entry_id
        assert data["title"] == new_summary

        self._recording_tests(entry_id, self.api.urls.schedule_entries)

    def test_schedules(self):
        # Get Schedule
        url = self.api.urls.schedules.get(project=self.project_id, schedule=self.schedule_id)
        data = self._get_data(url)
        assert data["id"] == self.schedule_id

    def test_templates(self):
        template_prefix = "BASECAMPY_TEST_TEMPLATE_"
        test_template_name = "%s%s" % (template_prefix, time.time())
        test_template_desc = "Created by Basecampy3"

        # Create a Template
        url = self.api.urls.templates.create(name=test_template_name,
                                             description=test_template_desc)
        data = self._get_data(url)
        template_id = data["id"]
        assert data["name"] == test_template_name
        assert "dock" in data

        # Get Template
        url = self.api.urls.templates.get(template=template_id)
        data = self._get_data(url)
        assert template_id == data["id"]

        # Update Template
        new_name = "%s_updated" % test_template_name
        new_desc = "%s_updated" % test_template_desc

        url = self.api.urls.templates.update(template=template_id,
                                             name=new_name,
                                             description=new_desc)
        data = self._get_data(url)
        assert template_id == data["id"]
        assert new_name == data["name"]
        assert new_desc == data["description"]

        # Create from Template (in Projects module)
        project_name = "%sfromTemplate%s" % (self.PROJECT_TEST_NAME_PREFIX, time.time())
        project_desc = "Basecampy test from template creation"
        url = self.api.urls.projects.create_from_template(
            template=template_id, name=project_name, description=project_desc
        )
        data = self._get_data(url)
        construction_id = data["id"]
        assert "status" in data

        max_attempts = 30
        # Get Construction Status (in Projects module)
        for attempt in range(1, max_attempts + 1):
            if attempt > 1:
                logger.info("Template Test: Attempt %s/%s...",
                            attempt, max_attempts)
            url = self.api.urls.projects.get_construction_status(
                template=template_id, project_construction=construction_id
            )
            data = self._get_data(url)
            assert data["id"] == construction_id
            if data["status"] == "completed":
                break
            elif data["status"] == "processing":
                time.sleep(1)
                continue
            else:
                raise AssertionError("Template Test: Unknown project "
                                     "construction status '%s'" % data["status"])
        else:
            raise AssertionError("Template Test: Project still under construction after %s attempts. Failure.")
        assert data["project"]["name"] == project_name
        assert data["project"]["description"] == project_desc

        project_id = data["project"]["id"]

        # trash this new template-created project
        url = self.api.urls.projects.trash(project=project_id)
        self._get_no_content(url)

        # List Templates
        url = self.api.urls.templates.list()
        data = self._get_data(url)
        assert len(data) > 0

        # Trash Templates that have the test prefix
        test_templates = [t for t in data if t["name"].startswith(template_prefix)]
        for template in test_templates:
            url = self.api.urls.templates.trash(template=template["id"])
            self._get_no_content(url)

        # List trashed Templates
        url = self.api.urls.templates.list(status="trashed")
        data = self._get_data(url)
        for d in data:
            if d["id"] == template_id:
                break
        else:
            raise AssertionError("Couldn't find trashed test template (ID=%s)" % template_id)

        logger.info("Successfully tested Project Templates!")

    def test_todo_sets(self):
        url = self.api.urls.todo_sets.get(project=self.project_id, todo_set=self.todoset_id)
        data = self._get_data(url)
        assert data["id"] == self.todoset_id
        logger.info("Successfully tested TodoSets!")

    def test_todo_collections(self):
        todolist_name = "Basecampy TodoList"
        todolist_desc = "Created during <strong>Basecampy</strong> unit tests."
        person_id = self._get_current_user()
        # Create TodoList
        url = self.api.urls.todo_lists.create(
            project=self.project_id, todo_set=self.todoset_id,
            name=todolist_name, description=todolist_desc
        )
        data = self._get_data(url)
        assert data["name"] == todolist_name
        assert data["description"] == todolist_desc

        todolist_id = data["id"]

        # Update TodoList
        new_list_name = "%s_updated" % todolist_name
        new_list_desc = "%s_updated" % todolist_desc
        url = self.api.urls.todo_lists.update(
            project=self.project_id, todolist=todolist_id,
            name=new_list_name, description=new_list_desc
        )
        data = self._get_data(url)
        assert data["id"] == todolist_id
        assert data["name"] == new_list_name
        assert data["description"] == new_list_desc

        # Create a To-do Item

        test_content = "A Basecampy thing to do"
        test_todo_desc = "Basecampy <strong>wuz</strong> <em>here</em>."
        data = self._create_todo_item(todolist_id, person_id, test_content, test_todo_desc)
        todo1 = data["id"]
        assert data["type"] == "Todo"
        assert len(data["assignees"]) > 0
        assert len(data['completion_subscribers']) > 0

        # Create a TodoGroup
        todogroup_name = "Basecampy3 Test Group"
        url = self.api.urls.todo_groups.create(project=self.project_id, todolist=todolist_id, name=todogroup_name)
        data = self._get_data(url)
        todogroup_id = data["id"]
        assert data["name"] == todogroup_name

        # List TodoGroups
        url = self.api.urls.todo_groups.list_by_todolist(project=self.project_id, todolist=todolist_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get TodoGroup
        url = self.api.urls.todo_groups.get(project=self.project_id, todogroup=todogroup_id)
        data = self._get_data(url)
        assert data["id"] == todogroup_id

        # Reposition TodoGroup
        url = self.api.urls.todo_groups.reposition(project=self.project_id,
                                                   todogroup=todogroup_id,
                                                   position=0)
        self._get_no_content(url)

        # Get To-do Item
        url = self.api.urls.todos.get(project=self.project_id, to_do=todo1)
        data = self._get_data(url)
        assert data["position"] == 1

        # Create a second To-do item in the To-do Group
        todo2_content = "Basecampy second thing to do"
        todo2_desc = "<strong>Something else</strong> you can delete actually."

        todo2 = self._create_todo_item(todogroup_id, person_id, todo2_content, todo2_desc)

        # List To-do Items by To-do List
        # in the To-do Group we made
        url = self.api.urls.todos.list_by_todolist(project=self.project_id, todolist=todogroup_id)
        data = self._get_data(url)
        assert len(data) > 0

        # in the To-do List we made
        url = self.api.urls.todos.list_by_todolist(project=self.project_id, todolist=todolist_id)
        data = self._get_data(url)
        assert len(data) > 0

        # "Complete" a To-do Item
        url = self.api.urls.todos.complete(project=self.project_id, to_do=todo1)
        self._get_no_content(url)

        # List completed To-do Items in the To-do List
        url = self.api.urls.todos.list_by_todolist(project=self.project_id,
                                                   todolist=todolist_id,
                                                   completed=True)
        data = self._get_data(url)
        assert len(data) > 0
        for todo in data:
            # should only have completed items
            assert todo["completed"] is True

        # "Uncomplete" a To-do Item
        url = self.api.urls.todos.uncomplete(project=self.project_id, to_do=todo1)
        self._get_no_content(url)

        # Update a To-do

        # first we will get the To-do Item so we can update it (omitting any
        # field in the To-do Item update will cause that field to get wiped/reset)
        url = self.api.urls.todos.get(project=self.project_id, to_do=todo1)
        data = self._get_data(url)

        new_content = "%s_updated" % data["content"]
        starts_on = date.today() + timedelta(days=1)
        due_on = starts_on + timedelta(days=1)

        url = self.api.urls.todos.update(
            project=self.project_id, to_do=todo1, content=new_content,
            description=data["description"], assignee_ids=data["assignees"],
            completion_subscriber_ids=data["completion_subscribers"],
            notify=True, due_on=due_on, starts_on=starts_on
        )

        data = self._get_data(url)
        assert data["id"] == todo1
        assert data["content"] == new_content
        assert data["due_on"] == due_on.strftime("%Y-%m-%d")
        assert data["starts_on"] == starts_on.strftime("%Y-%m-%d")

        # Reposition a To-do Item

        todo2_id = todo2["id"]
        url = self.api.urls.todos.reposition(project=self.project_id,
                                             to_do=todo2_id, position=1)
        self._get_no_content(url)

        # List To-do Lists
        url = self.api.urls.todo_lists.list_by_todoset(project=self.project_id, todo_set=self.todoset_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get To-do List
        url = self.api.urls.todo_lists.get(project=self.project_id, todolist=todolist_id)
        data = self._get_data(url)
        assert data["id"] == todolist_id
        assert data["name"] == new_list_name
        assert data["description"] == new_list_desc

        # perform Recording Tests on a To-do Item
        self._recording_tests(recording_id=todo1,
                              recording_urls=self.api.urls.todos,
                              test_visibility=False)

        # perform Recording Tests on a To-do Group
        self._recording_tests(recording_id=todogroup_id,
                              recording_urls=self.api.urls.todo_groups,
                              test_visibility=False)

        # perform Recording Tests on a To-do List
        self._recording_tests(recording_id=todolist_id,
                              recording_urls=self.api.urls.todo_lists)

    def test_uploads(self):
        uploaded_file_name = "awesome.png"
        # Create attachment
        data = self._create_attachment(uploaded_file_name)

        # Create Upload using the attachable_sgid we got
        data = self._create_upload(data["attachable_sgid"])

        assert data["title"] == uploaded_file_name

        # Get Upload
        upload_id = data["id"]
        data = self._get_upload(upload_id)

        assert data["title"] == uploaded_file_name

        # List uploads
        data = self._list_uploads()
        for upload in data:
            if upload["id"] == upload_id:
                break
        else:
            raise AssertionError("Did not find upload ID %s in vault ID %s" % (upload_id, self.vault_id))

        # Update upload
        new_name = "was-awesome"
        new_description = "A <strong>new</strong> description!"
        data = self._update_upload(upload_id, new_name, new_description)
        assert data["description"] == new_description

        # Perform Recording Tests
        self._recording_tests(upload_id, self.api.urls.uploads)

        logger.info("Successfully tested uploads (and attachments)!")

    def test_vaults(self):
        vault_name = "Basecampy3 Test Vault"
        # Create Vault
        url = self.api.urls.vaults.create(project=self.project_id, vault=self.vault_id, title=vault_name)
        data = self._get_data(url)
        assert data["title"] == vault_name
        test_vault_id = data["id"]

        # Update Vault
        new_vault_name = "Basecampy3 Renamed Test"

        url = self.api.urls.vaults.update(project=self.project_id, vault=test_vault_id, title=new_vault_name)
        data = self._get_data(url)
        assert data["id"] == test_vault_id
        assert data["title"] == new_vault_name

        # List Vaults in root Vault
        url = self.api.urls.vaults.list_vault_by_vault(project=self.project_id, vault=self.vault_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get Vault
        url = self.api.urls.vaults.get(project=self.project_id, vault=test_vault_id)
        data = self._get_data(url)
        assert data["id"] == test_vault_id
        assert data["title"] == new_vault_name

        # Perform Recording tests on the test vault
        self._recording_tests(recording_id=test_vault_id, recording_urls=self.api.urls.vaults)

        logger.info("Successfully tested vaults!")

    def test_webhooks(self):
        payload_url = "https://example.com/"
        # Create Webhook
        url = self.api.urls.webhooks.create(project=self.project_id,
                                            payload_url=payload_url,
                                            types=["Comment", "Vault"])
        data = self._get_data(url)
        assert data["payload_url"] == payload_url
        assert "Comment" in data["types"]
        assert "Vault" in data["types"]
        webhook_id = data["id"]

        # Update Webhook
        new_payload_url = "https://example.com/new/"
        new_types = ["Todo", "Todolist"]

        url = self.api.urls.webhooks.update(project=self.project_id,
                                            webhook=webhook_id,
                                            payload_url=new_payload_url,
                                            types=new_types, active=False)
        data = self._get_data(url)
        assert data["id"] == webhook_id
        assert data["payload_url"] == new_payload_url
        assert "Todo" in data["types"]
        assert "Todolist" in data["types"]

        # List Webhooks
        url = self.api.urls.webhooks.list(project=self.project_id)
        data = self._get_data(url)
        assert len(data) > 0

        # Get Webhooks
        url = self.api.urls.webhooks.get(project=self.project_id, webhook=webhook_id)
        data = self._get_data(url)
        assert data["id"] == webhook_id
        assert data["payload_url"] == new_payload_url
        assert "Todo" in data["types"]
        assert "Todolist" in data["types"]

        # Delete Webhook
        url = self.api.urls.webhooks.delete(project=self.project_id, webhook=webhook_id)
        self._get_no_content(url)

        logger.info("Successfully tested webhooks!")

    def _get_data(self, url):
        response = self._get_no_content(url)
        data = response.json()
        return data

    def _get_no_content(self, url):
        response = url.request(self.api.session)
        if not response.ok:
            raise exc.Basecamp3Error(response=response)
        return response

    def _recording_tests(self, recording_id, recording_urls, test_listing=True, test_archiving=True,
                         test_visibility=True, test_events=True,
                         test_subscriptions=True, trash=True):
        """
        Test all the different things Recordings support. Some Recordings do
        not support some functionality. Turn off tests for them so you don't
        get an error code.

        Comments do not support toggling client visibility for instance.

        :param recording_id: the ID of the Recording to be tested
        :type recording_id: int
        :param recording_urls: the URLs object on the API to use
        :type recording_urls: basecampy3.urls.endpoints.recordings.RecordingEndpointURLs
        :param test_visibility: whether or not to test visibility to clients
        :type test_visibility: bool
        """
        # Test List Recordings
        if test_listing:
            url = recording_urls.list(project=self.project_id)
            data = self._get_data(url)
            for rec in data:
                if rec["id"] == recording_id:
                    break
            else:
                raise AssertionError("Did not find recording ID %s in project ID %s"
                                     % (recording_id, self.project_id))

        if test_archiving:
            # Test Archive Recording
            url = recording_urls.archive(project=self.project_id, recording=recording_id)
            self._get_no_content(url)

            # Test Unarchive Recording
            url = recording_urls.unarchive(project=self.project_id, recording=recording_id)
            self._get_no_content(url)

        if test_visibility:
            for visibility in (True, False):
                url = recording_urls.client_visibility(project=self.project_id,
                                                       recording=recording_id,
                                                       visible_to_clients=visibility)
                data = self._get_data(url)
                assert data["visible_to_clients"] == visibility

        if test_events:
            url = recording_urls.events(project=self.project_id, recording=recording_id)
            data = self._get_data(url)
            # There should be at least one event in here. More like 6 or 7 after
            # all the things we did above.
            assert len(data) > 0
            event = data[0]
            assert event["recording_id"] == recording_id
            assert "action" in event

        if test_subscriptions:
            url = recording_urls.list_subscriptions(project=self.project_id, recording=recording_id)
            data = self._get_data(url)
            assert "subscribed" in data
            assert "count" in data

            url = recording_urls.subscribe_myself(project=self.project_id, recording=recording_id)
            _ = self._get_data(url)

            url = recording_urls.unsubscribe_myself(project=self.project_id, recording=recording_id)
            _ = self._get_no_content(url)

        # TODO
        # url = recording_urls.update_subscriptions(project=self.project_id, recording=recording_id)
        # data = self._get_data(url)
        # print(data)

        # Test Trash Recording
        if trash:
            url = recording_urls.trash(project=self.project_id, recording=recording_id)
            self._get_no_content(url)

    def _create_attachment(self, uploaded_file_name):
        dirname = os.path.dirname(__file__)
        test_file_path = os.path.join(dirname, self.UPLOAD_TEST_FILE_NAME)
        url = self.api.urls.attachments.create(test_file_path,
                                               uploaded_file_name)
        data = self._get_data(url)
        return data

    def _create_campfire_line(self, content):
        url = self.api.urls.campfire_lines.create(project=self.project_id,
                                                  campfire=self.campfire_id,
                                                  content=content)
        data = self._get_data(url)
        return data

    def _get_campfire_line(self, line_id):
        url = self.api.urls.campfire_lines.get(project=self.project_id,
                                               campfire=self.campfire_id,
                                               line=line_id)
        data = self._get_data(url)
        return data

    def _list_campfire_lines(self):
        url = self.api.urls.campfire_lines.list(project=self.project_id,
                                                campfire=self.campfire_id)
        data = self._get_data(url)
        return data

    def _create_upload(self, attachable_sgid):
        description = "This is a test file."
        url = self.api.urls.uploads.create(project=self.project_id,
                                           vault=self.vault_id,
                                           attachable_sgid=attachable_sgid,
                                           description=description)
        data = self._get_data(url)
        return data

    def _get_current_user(self):
        url = self.api.urls.people.get_myself()
        data = self._get_data(url)
        person_id = data["id"]
        assert "email_address" in data
        return person_id

    def _create_todo_item(self, todolist_id, person_id, content, desc):
        starts_on = date.today() + timedelta(days=1)
        due_on = starts_on + timedelta(days=1)

        url = self.api.urls.todos.create(
            project=self.project_id, todolist=todolist_id, content=content,
            description=desc, assignee_ids=[person_id],
            completion_subscriber_ids=[person_id], notify=True, due_on=due_on,
            starts_on=starts_on
        )
        data = self._get_data(url)
        assert data["starts_on"] == starts_on.strftime("%Y-%m-%d")
        assert data["due_on"] == due_on.strftime("%Y-%m-%d")

        return data

    def _get_upload(self, upload_id):
        url = self.api.urls.uploads.get(project=self.project_id, upload=upload_id)
        data = self._get_data(url)
        return data

    def _list_uploads(self):
        url = self.api.urls.uploads.list_by_vault(project=self.project_id, vault=self.vault_id)
        data = self._get_data(url)
        return data

    def _update_upload(self, upload_id, new_name, new_description):
        url = self.api.urls.uploads.update(project=self.project_id, upload=upload_id,
                                           base_name=new_name, description=new_description)
        data = self._get_data(url)
        return data


if __name__ == "__main__":
    unittest.main()
