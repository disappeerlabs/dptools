"""
test_verifier.py

Test suite for the Verifier gpg agent module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.gpg.agents import verifier
from dptools.gpg.agents import gpgagent
from dptools.gpg.agents import signer
from dptools.gpg.tests.data import common


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, verifier.gpgagent)


class TestVerifierClass(common.BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.key_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.v = verifier.Verifier(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.v, verifier.Verifier)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.v, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.v, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.v, name)
        self.assertTrue(check)

    def test_execute_method_valid(self):
        """
        TODO: this passes, but that is unexpected with incorrect passphrase
        Investigate for common test setup error as in other agent test modules
        """
        self.message = "Hello world."
        self.passphrase = 'passXXXXXXphrase'
        self.s = signer.Signer(self.keydir)
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase)
        result = self.v.execute(str(sig))
        self.assertTrue(result.valid)

    def test_execute_method_not_valid(self):
        self.message = "Hello world."
        result = self.v.execute(self.message)
        self.assertFalse(result.valid)