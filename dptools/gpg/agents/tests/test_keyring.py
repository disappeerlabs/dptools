"""
test_keyring.py

Test suite for the KeyRing module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import gnupg
from dptools.gpg.agents import gpgagent
from dptools.gpg.agents import keyring
from dptools.tests import basetestclass


class TestImports(unittest.TestCase):

    def test_gpg_agent_import(self):
        self.assertEqual(gpgagent, keyring.gpgagent)


class TestKeyRingBasics(basetestclass.BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.k = keyring.KeyRing(self.keydir)

    def test_instance(self):
        self.assertIsInstance(self.k, keyring.KeyRing)

    def test_is_instance_of_agent(self):
        self.assertIsInstance(self.k, gpgagent.GPGAgent)

    def test_keydir_attribute(self):
        self.assertEqual(self.keydir, self.k.home)

    def test_gpg_attribute(self):
        self.assertIsInstance(self.k.gpg, gnupg.GPG)


class TestKeyRingMethods(basetestclass.BaseTestClass):

    def setUp(self):
        self.keydir = self.key_dir_path
        self.mal = {'type': 'pub',
                    'trust': 'u',
                    'length': '2048',
                    'algo': '1',
                    'keyid': '191E11551232B305',
                    'date': '05/10/2020',
                    'expires': '04/01/2030',
                    'dummy': '',
                    'ownertrust': 'u',
                    'sig': '',
                    'uids': ['mal (no comment) <mallory@none.com>'],
                    'sigs': [],
                    'subkeys': [['5A11342E5AB0DE01', 'e', '1DAF59C9E688299CA6A274A25A11342E5AB0DE01']],
                    'fingerprint': '1AF427FA3F164D900D7B9913191E11551232B305'}
        self.k = keyring.KeyRing(self.keydir)

    def test_attribute_get_key_list(self):
        name = 'get_raw_key_list'
        result = hasattr(self.k, name)
        self.assertTrue(result)

    def test_get_key_list_returns_list(self):
        result = self.k.get_raw_key_list()
        self.assertIsInstance(result, gnupg.ListKeys)

    def test_result_get_raw_key_list(self):
        result = self.k.get_raw_key_list()
        target_fingerprints = [d['fingerprint'] for d in result]
        self.assertIn(self.mal['fingerprint'], target_fingerprints)

    def test_result_get_raw_key_list_secret(self):
        result = self.k.get_raw_key_list(secret=True)
        final = result[0]
        self.assertEqual(final['type'], 'sec')

    def test_attribute_export_method(self):
        name = 'export_key'
        check = hasattr(self.k, name)
        self.assertTrue(check)

    def test_result_export_method_fingerprint_valid(self):
        result = self.k.export_key(self.mal['fingerprint'])
        self.assertIn("PUBLIC KEY BLOCK", result)

    def test_result_export_method_fingerprint_not_valid(self):
        result = self.k.export_key('XXX666')
        self.assertEqual(0, len(result))

    def test_attribute_import_method(self):
        name = 'import_key'
        check = hasattr(self.k, name)
        self.assertTrue(check)

    def test_result_import_method_valid(self):
        pub_key = self.k.export_key(self.mal['fingerprint'])
        import tempfile
        with tempfile.TemporaryDirectory() as temp_home_dir:
            k = keyring.KeyRing(temp_home_dir)
            result = k.import_key(pub_key)
            self.assertTrue(result.count > 0)

    def test_result_import_method_not_valid(self):
        pub_key = 'xxx666'
        import tempfile
        with tempfile.TemporaryDirectory() as temp_home_dir:
            k = keyring.KeyRing(temp_home_dir)
            result = k.import_key(pub_key)
            self.assertTrue(result.count == 0)
