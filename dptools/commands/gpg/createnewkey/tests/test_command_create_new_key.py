"""
test_command_create_new_key.py	

Tests for the CreateNewKey command module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from unittest.mock import MagicMock, patch
from dptools.gpg.tests import helpers
from dptools.commands.gpg import createnewkey
from dptools.commands.gpg.createnewkey import (
    CreateNewKeyCommand,
    CreateNewKeyHandler,
    CreateNewKeyResult
)
from dptools.commands.tests import baseclasstestcommandpattern
gpg_agent_patch_path_string = 'dptools.commands.gpg.createnewkey.createnewkeycommand.GPGAgent'


@patch(gpg_agent_patch_path_string)
class TestCheckSanityWithBaseClass(baseclasstestcommandpattern.BaseClassTestCommandPattern):

    def config_register_callback(self):
        return createnewkey.register(self.mock_callback)

    def config_command(self):
        self.key_master = helpers.SetUpKeys()
        self.alice_key_input_dict = helpers.create_key_input_dict(helpers.key_reference_dict, helpers.alice_key_vals_dict)
        self.alice_dir_path = self.key_master.alice_dir_path
        command = CreateNewKeyCommand(self.alice_dir_path, self.alice_key_input_dict)
        return command

    def command_class(self):
        return CreateNewKeyCommand

    def handler_class(self):
        return CreateNewKeyHandler

    def result_class(self):
        return CreateNewKeyResult

    def setUp(self):
        super().setUp()

    def test_create_new_key_command_takes_key_path(self, *args):
        self.assertEqual(self.command.key_dir_path, self.alice_dir_path)

    def test_create_new_key_command_takes_key_input_dict(self, *args):
        self.assertEqual(self.command.key_input_dict, self.alice_key_input_dict)

    def test_result_from_queue_is_create_new_key_result(self, mock_agent):
        result = 'Hello there'
        target_method = mock_agent().gpg.gen_key = MagicMock(return_value=result)
        handler_class = self.command_map[self.command.name]
        # Initialize handler
        handler_object = handler_class(self.queue)
        # Run it
        handler_object.handle(self.command)
        # Get the result object, simulate polling queue
        result_obj = self.queue.get()
        self.assertEqual(result_obj.result, result)
