"""
baseclasstestcommandpattern.py

Base Class for Setting Up Generic Tests for Any Command Pattern Implementation
Subclass this for tests that are common to all command pattern implementations.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock
import queue
from dptools.commands import abstracts
import abc


class BaseClassTestCommandPattern(unittest.TestCase, metaclass=abc.ABCMeta):

    def setUp(self):
        self.queue = queue.Queue()
        self.mock_callback = MagicMock()
        self.mock_callback.handle = MagicMock()
        self.command_map = self.config_register_callback()
        self.command = self.config_command()

    @abc.abstractmethod
    def config_register_callback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def config_command(self):
        raise NotImplementedError

    @abc.abstractmethod
    def command_class(self):
        raise NotImplementedError

    @abc.abstractmethod
    def handler_class(self):
        raise NotImplementedError

    @abc.abstractmethod
    def result_class(self):
        raise NotImplementedError

    def test_command_instance(self, *args):
        self.assertTrue(issubclass(self.command_class(), abstracts.AbstractCommand))

    def test_handler_instance(self, *args):
        self.assertTrue(issubclass(self.handler_class(), abstracts.AbstractHandler))

    def test_result_instance(self, *args):
        self.assertTrue(issubclass(self.result_class(), abstracts.AbstractResult))

    def test_register_func_registers_callback_to_handle_method(self, *args):
        self.assertEqual(self.command_map[self.result_class().__name__].handle, self.mock_callback)

    def helper_get_result_from_queue(self, *args):
        # Grab the handler class from the map
        handler_class = self.command_map[self.command.name]
        # Initialize handler
        handler_object = handler_class(self.queue)
        # Run it
        handler_object.handle(self.command)
        # Get the result object, simulate polling queue
        result_obj = self.queue.get()
        return result_obj

    def test_handling_command_from_command_map_returns_result(self, *args):
        result_obj = self.helper_get_result_from_queue()
        # Results should be instance of result, generic to all commands
        self.assertIsInstance(result_obj, self.result_class())

    def test_handling_result_from_queue_calls_registered_callback(self, *args):
        result_obj = self.helper_get_result_from_queue()
        # Get result handler, instantiate, call handle with result
        result_handler_class = self.command_map[result_obj.name]
        result_handler_object = result_handler_class(self.queue)
        result_handler_object.handle(result_obj)
        # Our mock function should now be called
        self.assertTrue(self.mock_callback.called)
