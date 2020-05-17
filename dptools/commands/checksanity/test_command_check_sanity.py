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
from dptools.commands.checksanity import CheckSanityCommand
from dptools.commands.checksanity import CheckSanityHandler
from dptools.commands.checksanity import CheckSanityResult


class TestBasicsAndIntegrationFlow(unittest.TestCase):

    def setUp(self):
        self.queue = queue.Queue()
        self.mock_func = MagicMock()
        self.mock_func.handle = MagicMock()

    def test_check_sanity_command_instance(self):
        self.assertTrue(issubclass(CheckSanityCommand, abstracts.AbstractCommand))

    def test_check_sanity_handler_instance(self):
        self.assertTrue(issubclass(CheckSanityHandler, abstracts.AbstractHandler))

    def test_check_sanity_result_instance(self):
        self.assertTrue(issubclass(CheckSanityResult, abstracts.AbstractResult))

    def test_basic_integration_pattern_flow(self):
        # Register callback with command map
        self.command_map = checksanity.register_key_map(self.mock_func)

        # Define a Command
        self.msg = "Hello there"
        self.command = CheckSanityCommand(self.msg)

        # Grab the handler class from the map
        handler_class = self.command_map[self.command.name]
        # Initialize handler
        handler_object = handler_class(self.queue)
        # Run it
        handler_object.handle(self.command)

        # Get the result object, simulate polling queue
        result_obj = self.queue.get()

        # Result should be original message
        self.assertEqual(result_obj.result, self.msg)

        # Get result handler, instantiate, call handle with result
        result_handler_class = self.command_map[result_obj.name]
        result_handler_object = result_handler_class(self.queue)
        result_handler_object.handle(result_obj)

        # Our mock function should now be called
        self.assertTrue(self.mock_func.called)
