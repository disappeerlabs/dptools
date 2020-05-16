"""
test_signer.py

Test suite for the Signer module gpg agent class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import signer, gpgagent


class TestSignerBasics(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.keydir = self.key_master.alice_dir_path
        self.s = signer.Signer(self.keydir)

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, signer.gpgagent)

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


@unittest.skipIf(*mark.slow)
class TestSignerClassSlow(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.key_master.set_up_alice()
        self.fingerprint = self.key_master.alice_key['fingerprint']
        self.keydir = self.key_master.alice_dir_path
        self.message = "Hello world."
        self.s = signer.Signer(self.keydir)

    def test_execute_method_valid(self):
        result = self.s.execute(self.message, self.fingerprint, self.key_master.passphrase)
        self.assertIn("END PGP SIGNATURE", str(result))

    def test_execute_method_not_valid(self):
        result = self.s.execute(self.message, self.fingerprint, self.key_master.bad_passphrase)
        self.assertIsNone(result.status)

    def test_execute_method_valid_detached(self):
        result = self.s.execute(self.message,
                                self.fingerprint,
                                self.key_master.passphrase,
                                detach=True)
        self.assertNotIn(self.message, str(result))
