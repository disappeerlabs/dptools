"""
test_command_check_sanity.py	

Tests for the check sanity command implementation

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import queue
from dptools.commands import abstracts
from dptools.commands import checksanity
from dptools.commands.checksanity.checksanitycommand import (
    CheckSanityCommand,
    CheckSanityHandler,
    CheckSanityResult
)


class TestBasicsAndIntegrationFlow(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.mock_callback = MagicMock()
        self.mock_callback.handle = MagicMock()
        # Register callback with command map
        self.command_map = checksanity.register(self.mock_callback)
        # Define a Command
        self.msg = "Hello there"
        self.command = CheckSanityCommand(self.msg)

    def test_check_sanity_command_instance(self):
        self.assertTrue(issubclass(CheckSanityCommand, abstracts.AbstractCommand))

    def test_check_sanity_handler_instance(self):
        self.assertTrue(issubclass(CheckSanityHandler, abstracts.AbstractHandler))

    def test_check_sanity_result_instance(self):
        self.assertTrue(issubclass(CheckSanityResult, abstracts.AbstractResult))

    def test_check_sanity_register_func_registers_callback_to_handle_method(self):
        target_dict = checksanity.register(self.mock_callback)
        self.assertEqual(target_dict[CheckSanityResult.__name__].handle, self.mock_callback)

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

    def test_handling_command_from_command_map_returns_result(self):
        result_obj = self.helper_get_result_from_queue()
        # Results should be instance of result, generic to all commands
        self.assertIsInstance(result_obj, CheckSanityResult)
        # Result should be original message, specific to this command
        self.assertEqual(result_obj.result, self.msg)

    def test_handling_result_from_queue_calls_registered_callback(self):
        result_obj = self.helper_get_result_from_queue()
        # Get result handler, instantiate, call handle with result
        result_handler_class = self.command_map[result_obj.name]
        result_handler_object = result_handler_class(self.queue)
        result_handler_object.handle(result_obj)
        # Our mock function should now be called
        self.assertTrue(self.mock_callback.called)
