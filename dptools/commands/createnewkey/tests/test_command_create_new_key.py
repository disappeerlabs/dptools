"""
test_command_create_new_key.py	

Tests for the CreateNewKey command module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
import queue
from dptools.gpg.tests import helpers
from dptools.commands import abstracts
from dptools.commands import createnewkey
from dptools.commands.createnewkey.createnewkeycommand import (
    CreateNewKeyCommand,
    CreateNewKeyHandler,
    CreateNewKeyResult
)


class TestBasics(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.mock_callback = MagicMock()
        self.mock_callback.handle = MagicMock()
        # Register callback with command map
        self.command_map = createnewkey.register(self.mock_callback)
        # Define command
        self.key_master = helpers.SetUpKeys()
        self.alice_key_input_dict = helpers.create_key_input_dict(helpers.key_reference_dict, helpers.alice_key_vals_dict)
        self.alice_dir_path = self.key_master.alice_dir_path
        self.command = CreateNewKeyCommand(self.alice_dir_path, self.alice_key_input_dict)

    def test_create_new_key_command_instance(self):
        self.assertTrue(issubclass(CreateNewKeyCommand, abstracts.AbstractCommand))

    def test_create_new_key_handler_instance(self):
        self.assertTrue(issubclass(CreateNewKeyHandler, abstracts.AbstractHandler))

    def test_create_new_key_result_instance(self):
        self.assertTrue(issubclass(CreateNewKeyResult, abstracts.AbstractResult))

    def test_create_new_key_command_takes_key_path(self):
        self.assertEqual(self.command.key_dir_path, self.alice_dir_path)

    def test_create_new_key_command_takes_key_input_dict(self):
        self.assertEqual(self.command.key_input_dict, self.alice_key_input_dict)

    def test_create_new_key_register_func_registers_callback_to_handle_method(self):
        target_dict = createnewkey.register(self.mock_callback)
        self.assertEqual(target_dict[CreateNewKeyResult.__name__].handle, self.mock_callback)

    def helper_get_result_from_queue(self):
        # Grab the handler class from the map
        handler_class = self.command_map[self.command.name]
        # Initialize handler
        handler_object = handler_class(self.queue)
        # Run it
        handler_object.handle(self.command)
        # Get the result object, simulate polling queue
        result_obj = self.queue.get()
        return result_obj

    @patch('dptools.commands.createnewkey.createnewkeycommand.GPGAgent')
    def test_handling_command_from_command_map_returns_result(self, mocked):
        result_obj = self.helper_get_result_from_queue()
        # Results should be instance of result, generic to all commands
        self.assertIsInstance(result_obj, CreateNewKeyResult)

    @patch('dptools.commands.createnewkey.createnewkeycommand.GPGAgent')
    def test_handling_result_from_queue_calls_registered_callback(self, mocked):
        result_obj = self.helper_get_result_from_queue()
        # Get result handler, instantiate, call handle with result
        result_handler_class = self.command_map[result_obj.name]
        result_handler_object = result_handler_class(self.queue)
        result_handler_object.handle(result_obj)
        # Our mock function should now be called
        self.assertTrue(self.mock_callback.called)

    @patch('dptools.commands.createnewkey.createnewkeycommand.GPGAgent')
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
