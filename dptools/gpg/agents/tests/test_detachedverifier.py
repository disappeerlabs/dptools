"""
test_detachedverifier.py

Test suite for the DetachedVerifier class object and module

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.gpg.agents import detachedverifier
from dptools.gpg.agents import gpgagent
from dptools.gpg.agents import signer
from dptools.gpg.tests.data import common
import tempfile


class TestImports(unittest.TestCase):

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, detachedverifier.gpgagent)


class TestVerifierClass(common.BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.key_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.x = detachedverifier.DetachedVerifier(self.keydir)

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

    def test_execute_method_valid(self):
        self.message = "Hello world."
        self.passphrase = 'passphrase'
        self.s = signer.Signer(self.keydir)
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase, detach=True)
        data = bytes(self.message, 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes(str(sig), 'utf-8'))
            tmp_file.seek(0)
            verify_detached = self.x.execute(tmp_file.name, data)
        self.assertTrue(verify_detached.valid)

    def test_execute_method_not_valid(self):
        # Use alt key dir path for signer to make test pass
        self.s = signer.Signer(self.alt_key_dir_path)
        self.message = "Hello world."
        self.passphrase = 'passsphrase'
        sig = self.s.execute(self.message, self.key_fingerprint, self.passphrase, detach=True)
        data = bytes(self.message, 'utf-8')
        with tempfile.NamedTemporaryFile() as tmp_file:
            tmp_file.write(bytes(str(sig), 'utf-8'))
            tmp_file.seek(0)
            verify_detached = self.x.execute(tmp_file.name, data)
        self.assertFalse(verify_detached.valid)
