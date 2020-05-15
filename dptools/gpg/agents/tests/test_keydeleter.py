"""
test_keydeleter.py

Test suite for KeyDeleter gpgagent module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.agents import keydeleter
from dptools.gpg.agents import gpgagent


class TestKeyDeleterClassBasics(unittest.TestCase):

    def setUp(self):
        self.d = keydeleter.KeyDeleter(None)

    def test_gpgagent_import(self):
        self.assertEqual(gpgagent, keydeleter.gpgagent)

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


@unittest.skipIf(*mark.slow)
class TestKeyDeleterClassLongRunning(unittest.TestCase):

    def setUp(self):
        self.key_master = helpers.SetUpKeys()
        self.key_master.set_up_alice()
        self.fingerprint = self.key_master.alice_key['fingerprint']
        self.keydir = self.key_master.alice_dir_path
        self.d = keydeleter.KeyDeleter(self.keydir)

    def test_execute_method_delete_own_secret_key(self):
        before_len = len(self.d.gpg.list_keys())
        result = self.d.execute(self.fingerprint, secret=True, passphrase=self.key_master.passphrase)
        after_len = len(self.d.gpg.list_keys())
        self.assertEqual(after_len - before_len, -1)

    def test_execute_method_delete_others_key(self):
        self.key_master.set_up_bob()
        self.key_master.alice_gpg.import_keys(self.key_master.bob_export)
        bob_fingerprint = self.key_master.bob_key['fingerprint']
        before_len = len(self.d.gpg.list_keys())
        result = self.d.execute(bob_fingerprint)
        after_len = len(self.d.gpg.list_keys())
        self.assertEqual(after_len - before_len, -1)
