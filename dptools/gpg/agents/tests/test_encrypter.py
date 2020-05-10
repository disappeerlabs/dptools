"""
test_encrypter.py

Test suite for the Encrypter gpg agent module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import os
from unittest.mock import MagicMock
from dptools.gpg.agents import encrypter
from dptools.gpg.agents import gpgagent
from dptools.gpg.tests.data import keys, altkeys


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, encrypter.gpgagent)


class BaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_path = os.path.dirname(keys.__file__)
        cls.alt_key_dir_path = os.path.dirname(altkeys.__file__)


class TestKeyMakerClass(BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.key_fingerprint = 'xxxxx'
        self.message = "Hello world."
        self.e = encrypter.Encrypter(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.e, encrypter.Encrypter)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.e, gpgagent.GPGAgent)

    def test_key_attribute(self):
        name = 'gpg'
        check = hasattr(self.e, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.e, name)
        self.assertTrue(check)

    def test_execute_calls_encrypt_with_args(self):
        sub = self.e.gpg.encrypt = MagicMock()
        self.e.execute(self.message, self.key_fingerprint)
        sub.assert_called_with(self.message, self.key_fingerprint, always_trust=True)

    def test_execute_returns_result(self):
        sub = self.e.gpg.encrypt = MagicMock(return_value='hello')
        result = self.e.execute(self.message, self.key_fingerprint)
        self.assertEqual(result, sub.return_value)