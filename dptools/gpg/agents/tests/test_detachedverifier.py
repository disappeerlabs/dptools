"""
test_detachedverifier.py

Test suite for the DetachedVerifier class object and module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import tempfile
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import detachedverifier, gpgagent, signer


class TestVerifierClass(unittest.TestCase):

    def setUp(self):
        self.x = detachedverifier.DetachedVerifier(None)

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, detachedverifier.gpgagent)

    def test_instance(self):
        self.assertIsInstance(self.x, detachedverifier.DetachedVerifier)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.x, gpgagent.GPGAgent)

    def test_gpg_attribute(self):
        name = 'gpg'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_execute_attribute(self):
        name = 'execute'
        check = hasattr(self.x, name)
        self.assertTrue(check)


@unittest.skipIf(*mark.slow)
class TestVerifierClassSlow(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.key_master.set_up_alice()
        self.fingerprint = self.key_master.alice_key['fingerprint']
        self.keydir = self.key_master.alice_dir_path
        self.message = "Hello world."
        self.s = signer.Signer(self.keydir)
        self.verifier = detachedverifier.DetachedVerifier(self.keydir)

    def test_execute_method_valid(self):
        sig = self.sign(self.key_master.passphrase)
        verify_detached = self.write_to_tmp_file(sig)
        self.assertTrue(verify_detached.valid)

    def test_execute_method_not_valid(self):
        sig = self.sign(self.key_master.bad_passphrase)
        verify_detached = self.write_to_tmp_file(sig)
        self.assertFalse(verify_detached.valid)

    def sign(self, passphrase):
        return self.s.execute(self.message, self.fingerprint, passphrase, detach=True)

    def write_to_tmp_file(self, signature):
        data = bytes(self.message, 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes(str(signature), 'utf-8'))
            tmp_file.seek(0)
            verify_detached = self.verifier.execute(tmp_file.name, data)
        return verify_detached
