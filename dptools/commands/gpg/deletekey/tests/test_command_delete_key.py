"""
test_command_delete_key.py	

Test module for Command GPG Delete Key

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

from unittest.mock import MagicMock, patch
from dptools.gpg.tests import helpers
from dptools.commands.gpg import deletekey
from dptools.commands.gpg.deletekey.deletekeycommand import (
    DeleteKeyCommand,
    DeleteKeyHandler,
    DeleteKeyResult
)
from dptools.commands.tests import baseclasstestcommandpattern
gpg_agent_patch_path_string = 'dptools.commands.gpg.deletekey.deletekeycommand.KeyDeleter'


class TestDeleteKeyWithBaseClass(baseclasstestcommandpattern.BaseClassTestCommandPattern):

    def config_register_callback(self):
        return deletekey.register(self.mock_callback)

    def config_command(self):
        self.key_master = helpers.SetUpKeys()
        self.key_dir_path = self.key_master.alice_dir_path
        self.key_fingerprint_list = []
        self.secret = True
        self.passphrase = 'passphrase'
        command = DeleteKeyCommand(key_dir_path=self.key_dir_path,
                                   key_fingerprint_list=self.key_fingerprint_list,
                                   secret=self.secret,
                                   passphrase=self.passphrase)
        return command

    def command_class(self):
        return DeleteKeyCommand

    def handler_class(self):
        return DeleteKeyHandler

    def result_class(self):
        return DeleteKeyResult

    def setUp(self):
        super().setUp()

    def test_delete_command_takes_key_dir_path_arg(self):
        self.assertEqual(self.key_dir_path, self.command.key_dir_path)

    def test_delete_command_takes_key_fingerprint_list_arg(self):
        self.assertEqual(self.key_fingerprint_list, self.command.key_fingerprint_list)

    def test_delete_command_takes_secret_arg(self):
        self.assertEqual(self.secret, self.command.secret)

    def test_delete_command_takes_passphrase_arg(self):
        self.assertEqual(self.passphrase, self.command.passphrase)

    @patch(gpg_agent_patch_path_string)
    def test_result_attr_is_output_of_delete_execute(self, mock_agent):
        val = 'hello there'
        target_method = mock_agent().execute = MagicMock(return_value=val)
        result_obj = self.helper_get_result_from_queue()
        self.assertEqual(result_obj.result, val)
