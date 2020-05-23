"""
test_command_create_new_key.py	

Tests for the CreateNewKey command module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import queue
from dptools.gpg.tests import helpers
from dptools.commands import abstracts
from dptools.commands import createnewkey
from dptools.commands.createnewkey import CreateNewKeyCommand, CreateNewKeyHandler, CreateNewKeyResult


class TestBasics(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.alice_key_input_dict = helpers.create_key_input_dict(helpers.key_reference_dict, helpers.alice_key_vals_dict)
        self.alice_dir_path = self.key_master.alice_dir_path
        self.queue = queue.Queue()
        self.mock_func = MagicMock()
        self.mock_func.handle = MagicMock()
        self.create_key_command = CreateNewKeyCommand(self.alice_dir_path, self.alice_key_input_dict)

    def test_create_new_key_command_instance(self):
        self.assertTrue(issubclass(CreateNewKeyCommand, abstracts.AbstractCommand))

    def test_create_new_key_handler_instance(self):
        self.assertTrue(issubclass(CreateNewKeyHandler, abstracts.AbstractHandler))

    def test_create_new_key_result_instance(self):
        self.assertTrue(issubclass(CreateNewKeyResult, abstracts.AbstractResult))

    def test_create_new_key_command_takes_key_path(self):
        self.assertEqual(self.create_key_command.key_dir_path, self.alice_dir_path)

    def test_create_new_key_command_takes_key_input_dict(self):
        self.assertEqual(self.create_key_command.key_input_dict, self.alice_key_input_dict)

    def test_continue_here(self):
        # TODO: continue working on create new key from here
        self.assertTrue(True)
