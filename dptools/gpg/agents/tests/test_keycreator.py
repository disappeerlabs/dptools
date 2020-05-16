"""
test_keycreator.py

Test suite for KeyCreator module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import queue
import threading
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from dptools import gpg
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import keycreator
from dptools.gpg.agents import gpgagent
from dptools.static import constants


class TestImportsAndConstants(unittest.TestCase):

    def test_gpgagent(self):
        self.assertEqual(gpgagent, keycreator.gpgagent)

    def test_threading(self):
        self.assertEqual(threading, keycreator.threading)

    def test_constants(self):
        self.assertEqual(constants, keycreator.constants)

    def test_constants_command_list(self):
        target = constants.command_list
        self.assertEqual(target, keycreator.command_list)


class BaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_temp = tempfile.TemporaryDirectory()
        cls.key_dir_path = cls.key_dir_temp.name

    @classmethod
    def tearDownClass(cls):
        cls.key_dir_temp.cleanup()


class TestKeyCreatorClass(BaseTestClass):

    def setUp(self):
        self.queue = queue.Queue()
        self.keydir = self.key_dir_path
        self.key_input = helpers.create_key_input_dict(helpers.key_reference_dict, helpers.alice_key_vals_dict)
        self.x = keycreator.KeyCreator(self.keydir, self.queue)

    def test_instance(self):
        self.assertIsInstance(self.x, keycreator.KeyCreator)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.x, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_queue_attribute_set(self):
        self.assertEqual(self.x.queue, self.queue)

    def test_execute_method_attribute(self):
        name = 'execute'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_create_new_key_worker_method_attribute(self):
        name = '_create_new_key_worker'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    @patch('dptools.gpg.agents.keycreator.threading')
    def test_execute_calls_thread(self, mocked):
        mocked.Thread = MagicMock()
        self.x.execute(self.key_input)
        self.assertTrue(mocked.Thread.called)

    @patch.object(gpg.agents.keycreator.threading.Thread, 'start')
    def test_execute_calls_thread_start(self, mocked1):
        self.x.execute(self.key_input)
        self.assertTrue(mocked1.called)

    @unittest.skipIf(*mark.slow)
    def test_create_new_key_method(self):
        before = self.x.gpg.list_keys()
        before_len = len(before)
        result = self.x._create_new_key_worker(self.key_input)
        after = self.x.gpg.list_keys()
        after_len = len(after)
        self.assertEqual(after_len - before_len, 1)

    def test_create_new_key_worker_puts_to_queue(self):
        target = "xxxxxyyyyyzzzzzz"
        self.x.gpg = MagicMock()
        self.x.gpg.gen_key = MagicMock(return_value=target)
        result = self.x._create_new_key_worker(dict())
        got = self.queue.get()
        comp = dict(desc=constants.command_list.Create_New_Key, result=target)
        self.assertEqual(comp, got)
