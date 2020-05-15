"""
test_decrypter.py

Test suite for Decrypter gpg agent module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import decrypter, gpgagent, encrypter


class TestDecrypterClass(unittest.TestCase):

    def setUp(self):
        self.d = decrypter.Decrypter(None)

    def test_gpg_agent_import(self):
        self.assertEqual(gpgagent, decrypter.gpgagent)

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


@unittest.skipIf(*mark.slow)
class TestDecrypterClassSlow(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.key_master.set_up_alice()
        self.fingerprint = self.key_master.alice_key['fingerprint']
        self.keydir = self.key_master.alice_dir_path
        self.message = "Hello world."
        self.encrypter = encrypter.Encrypter(self.keydir)
        encrypt_result = self.encrypter.execute(self.message, self.fingerprint)
        self.ciphertext = str(encrypt_result)
        self.d = decrypter.Decrypter(self.keydir)

    def test_decrypt_message_result_valid_passphrase(self):
        result = self.d.execute(self.ciphertext, self.key_master.passphrase)
        self.assertTrue(result.ok)

    def test_decrypt_message_result_not_valid_passphrase(self):
        result = self.d.execute(self.ciphertext, self.message)
        self.assertFalse(result.ok)
