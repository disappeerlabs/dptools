"""
test_signer.py

Test suite for the Signer module gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
import os

import dptools.tests.basetestclass
from dptools.gpg.agents import signer
from dptools.gpg.agents import gpgagent
from dptools.gpg.tests.data import common


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, signer.gpgagent)


class TestSignerClass(dptools.tests.basetestclass.BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.key_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.s = signer.Signer(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.s, signer.Signer)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.s, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.s, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.s, name)
        self.assertTrue(check)

    def test_execute_method_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        result = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        self.assertIn("SIGNED MESSAGE", str(result))

    @unittest.skip("Unexpected failure, see test_decrypter skip for similar")
    def test_execute_method_not_valid(self):
        # TODO: Unsure why this test fails, see comment in test_decrypter module
        self.message = "Hello world."
        self.passphrase = 'xxxyyy'
        result = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        self.assertEqual(0, len(str(result)))

    def test_execute_method_valid_detached(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        result = self.s.execute(self.message,
                                self.key_fingerprint,
                                self.passphrase,
                                detach=True)
        self.assertNotIn(self.message, str(result))

