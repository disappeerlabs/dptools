"""
test_verifier.py

Test suite for the Verifier gpg agent module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import verifier, signer, gpgagent


class TestVerifierClass(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.keydir = self.key_master.alice_dir_path
        self.v = verifier.Verifier(self.keydir)

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, verifier.gpgagent)

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


@unittest.skipIf(*mark.slow)
class TestVerifierClassSlow(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.key_master.set_up_alice()
        self.keydir = self.key_master.alice_dir_path
        self.message = "Hello world."
        self.key_fingerprint = self.key_master.alice_key['fingerprint']
        self.v = verifier.Verifier(self.keydir)

    def test_execute_method_valid(self):
        s = signer.Signer(self.keydir)
        sig = s.execute(self.message, self.key_fingerprint, self.key_master.passphrase)
        result = self.v.execute(str(sig))
        self.assertTrue(result.valid)

    def test_execute_method_not_valid(self):
        result = self.v.execute(self.message)
        self.assertFalse(result.valid)
