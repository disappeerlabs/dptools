"""
test_decrypter.py

Test suite for Decrypter gpg agent module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import os
from dptools.gpg.agents import decrypter
from dptools.gpg.agents import gpgagent
from dptools.gpg.agents import encrypter
from dptools.gpg.tests.data import keys


class TestImports(unittest.TestCase):

    def test_gpg_agent_import(self):
        self.assertEqual(gpgagent, decrypter.gpgagent)


class BaseTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_path = os.path.dirname(keys.__file__)


class TestDecrypterClass(BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.key_fingerprint = '1AF427FA3F164D900D7B9913191E11551232B305'
        self.d = decrypter.Decrypter(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.d, decrypter.Decrypter)

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

    def test_decrypt_message_result_valid_passphrase(self):
        self.encrypter = encrypter.Encrypter(self.keydir)
        self.message = "Hello world."
        encrypt_result = self.encrypter.execute(self.message, self.key_fingerprint)
        self.ciphertext = str(encrypt_result)
        self.passphrase = 'passphrase'
        result = self.d.execute(self.ciphertext, self.passphrase)
        self.assertTrue(result.ok)

    @unittest.skip("Logic failure in the test")
    def test_decrypt_message_result_not_valid_passphrase(self):
        """
        TODO: Resolve logic issue.
        Expected not to decrypt, but it does.
        May be setup error, because encrypt/decrypt agents are:
            - both use the same keyring
            - therefore are same user?
            - therefore we can decrypt even when the passphrase is wrong???
        """
        self.encrypter = encrypter.Encrypter(self.keydir)
        self.message = "Hello world."
        encrypt_result = self.encrypter.execute(self.message, self.key_fingerprint)
        self.ciphertext = str(encrypt_result)
        self.passphrase = 'passphddddrase'
        result = self.d.execute(self.ciphertext, self.passphrase)
        self.assertFalse(result.ok)
