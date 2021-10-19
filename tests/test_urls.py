# -*- coding: utf-8 -*-
"""
Tests for the basecampy3.urls package.
"""

import logging
import os
import re
import time
import unittest
import uuid

from basecampy3 import Basecamp3, exc

logger = logging.getLogger("basecampy3")
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


class APITest(unittest.TestCase):
    PROJECT_TEST_NAME_PREFIX = "_DELETE_pytest__basecampy3_"
    PROJECT_TEST_DESCRIPTION = "Trash me I am a test project."
    UPLOAD_TEST_FILE_NAME = "testfile.png"

    def setUp(self):
        self.api = Basecamp3()
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
        campfire_lines = self.api.urls.campfire_lines
        test_text = "Good morning!"

        # Create Campfire Line
        data = self._create_campfire_line(test_text)
        line_id = data["id"]
        assert data["content"] == test_text

        # Get Campfire Line
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

    def _get_data(self, url):
        response = self._get_no_content(url)
        data = response.json()
        return data

    def _get_no_content(self, url):
        response = url.request(self.api.session)
        if not response.ok:
            raise exc.Basecamp3Error(response=response)
        return response

    def _recording_tests(self, recording_id, recording_urls, test_visibility=True, trash=True):
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
        url = recording_urls.list(project=self.project_id)
        data = self._get_data(url)
        for rec in data:
            if rec["id"] == recording_id:
                break
        else:
            raise AssertionError("Did not find recording ID %s in project ID %s"
                                 % (recording_id, self.project_id))

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

        url = recording_urls.events(project=self.project_id, recording=recording_id)
        data = self._get_data(url)
        # There should be at least one event in here. More like 6 or 7 after
        # all the things we did above.
        assert len(data) > 0
        event = data[0]
        assert event["recording_id"] == recording_id
        assert "action" in event

        url = recording_urls.list_subscriptions(project=self.project_id, recording=recording_id)
        data = self._get_data(url)
        assert "subscribed" in data
        assert "count" in data

        url = recording_urls.subscribe_myself(project=self.project_id, recording=recording_id)
        data = self._get_data(url)

        url = recording_urls.unsubscribe_myself(project=self.project_id, recording=recording_id)
        data = self._get_no_content(url)

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
