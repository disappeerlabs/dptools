"""
test_threaddispatcher.py

Test module for ThreadDispatcher, Abstract Handler wrapper for dispatching concrete command to thread.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from dptools.commands.checksanity import CheckSanityCommand, CheckSanityHandler
from dptools.commands.wrappers import threaddispatcher


class TestThreadDispatcher(unittest.TestCase):

    def setUp(self):
        self.mock_queue = MagicMock()
        self.mock_handler = MagicMock()
        self.inner_handle = self.mock_handler.handle = MagicMock()
        self.check_sanity_command = CheckSanityCommand("Hello There")
        self.check_sanity_handler = CheckSanityHandler(self.mock_queue)
        self.x = threaddispatcher.ThreadDispatchDecorator(self.mock_queue, self.check_sanity_handler)

    def test_metaclass_attribute(self):
        check = hasattr(self.x, '_abc_impl')
        self.assertTrue(check)

    def test_handler_has_queue_attr_set(self):
        self.assertEqual(self.mock_queue, self.x.destination_queue)

    def test_handler_has_handle_method(self):
        self.assertTrue(hasattr(self.x, 'handle'))

    def test_abstract_handler_method_takes_arg(self):
        mock_command = MagicMock()
        try:
            self.x.handle(mock_command)
        except:
            self.assertTrue(False, "handle method should take arg")

    @patch('dptools.commands.wrappers.threaddispatcher.threading')
    def test_execute_calls_thread(self, mocked):
        mocked.Thread = MagicMock()
        self.x.handle(self.check_sanity_command)
        self.assertTrue(mocked.Thread.called)
        mocked.Thread.assert_called_with(name=self.check_sanity_command.name, target=self.check_sanity_handler.handle, args=(self.check_sanity_command,))
