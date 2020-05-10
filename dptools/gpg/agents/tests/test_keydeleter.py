"""
test_keydeleter.py

Test suite for KeyDeleter gpgagent module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import tempfile
from dptools.gpg.agents.tests.test_keycreator import create_key_input_dict, new_key_default_vals_dict, new_key_input_dict
from dptools.gpg.agents import keydeleter, keycreator
from dptools.gpg.agents import gpgagent


class TestImports(unittest.TestCase):

    def test_gpgagent(self):
        self.assertEqual(gpgagent, keydeleter.gpgagent)


class TestKeyDeleterClassBasics(unittest.TestCase):

    def setUp(self):
        self.keydir_obj = tempfile.TemporaryDirectory()
        self.keydir = self.keydir_obj.name
        self.d = keydeleter.KeyDeleter(self.keydir)

    def tearDown(self):
        self.keydir_obj.cleanup()

    def test_instance(self):
        self.assertIsInstance(self.d, keydeleter.KeyDeleter)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.d, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.d, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.d, name)
        self.assertTrue(check)


class TestKeyDeleterClassLongRunning(unittest.TestCase):

    def setUp(self):
        self.keydir_obj = tempfile.TemporaryDirectory()
        self.keydir = self.keydir_obj.name
        self.d = keydeleter.KeyDeleter(self.keydir)
        key_input_dict = create_key_input_dict(new_key_input_dict, new_key_default_vals_dict)
        input_data = self.d.gpg.gen_key_input(**key_input_dict)
        result = self.d.gpg.gen_key(input_data)

    def tearDown(self):
        self.keydir_obj.cleanup()

    @unittest.skip("Skip key deletion, requires lengthy key creation")
    def test_execute_method(self):
        before = self.d.gpg.list_keys()
        before_len = len(before)
        target = before[0]['fingerprint']
        result = self.d.execute(target, secret=True, passphrase='passphrase')
        after = self.d.gpg.list_keys()
        after_len = len(after)
        self.assertEqual(after_len - before_len, -1)
