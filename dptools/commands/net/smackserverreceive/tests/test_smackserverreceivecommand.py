"""
test_smackserverreceivecommand.py	

> Test cases for the smack server receive command.

The presumption here is that the smack server is:
    - putting a result to the queue, rather than a command
    - so the controller with queue will only need to register a callback for the result
Therefore:
    - this is not a complete command implementation
    - tests do not use the base test class for the complete pattern



Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from dptools.commands import abstracts
from dptools.commands.tests import baseclasstestcommandpattern
from dptools.commands.net import smackserverreceive
from dptools.commands.net.smackserverreceive.smackserverreceivecommand import (
    SmackServerReceiveResult
)


class TestSmackServerReceiveResult(unittest.TestCase):

    def setUp(self):
        self.mock_result = MagicMock()
        self.x = SmackServerReceiveResult(self.mock_result)

    def test_abstract_instance(self):
        self.assertIsInstance(self.x, abstracts.AbstractResult)

    def test_instance(self):
        self.assertIsInstance(self.x, SmackServerReceiveResult)

    def test_instance_sets_result(self):
        self.assertEqual(self.mock_result, self.x.result)


class TestRegisterFunction(unittest.TestCase):

    def setUp(self):
        self.mock_callback = MagicMock()
        self.x = smackserverreceive.register(self.mock_callback)

    def test_register_result(self):
        self.assertIsInstance(self.x, dict)

    def test_register_func_maps_callback_to_handle_method(self):
        self.assertEqual(self.x[smackserverreceive.SmackServerReceiveResult.__name__].handle, self.mock_callback)
