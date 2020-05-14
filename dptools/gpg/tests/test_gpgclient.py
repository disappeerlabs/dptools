"""
test_gpgclient.py

Test suite for the GPGClient module and class object.

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import unittest
from unittest.mock import MagicMock, patch
from dptools.gpg.tests import basegpgtestclass
from dptools.gpg import gpgclient
from dptools.gpg.agents import keyring
from dptools.gpg.agents import encrypter
from dptools.gpg.agents import decrypter
from dptools.gpg.agents import signer
from dptools.gpg.agents import verifier
from dptools.gpg.helpers import keyfinder
from dptools.gpg.tests.data import common


class TestImports(unittest.TestCase):

    def test_keyring(self):
        self.assertEqual(keyring, gpgclient.keyring)

    def test_keyfinder(self):
        self.assertEqual(keyfinder, gpgclient.keyfinder)

    def test_encrypter(self):
        self.assertEqual(encrypter, gpgclient.encrypter)

    def test_decrypter(self):
        self.assertEqual(decrypter, gpgclient.decrypter)

    def test_signer(self):
        self.assertEqual(signer, gpgclient.signer)

    def test_verifier(self):
        self.assertEqual(verifier, gpgclient.verifier)


class TestGPGClientClassBasics(basegpgtestclass.BaseGPGTestClass):

    def setUp(self):
        self.alt_key_dir = self.alt_key_dir_path
        self.key_dir = self.key_dir_path
        self.key_id = '12345'
        self.message = "Hello"
        self.passphrase = 'passphrase'
        self.valid_keyid = common.current_key_keyid_keys_dir_ring
        self.valid_key_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.x = gpgclient.GPGClient(self.key_dir)

    def test_instance(self):
        self.assertIsInstance(self.x, gpgclient.GPGClient)

    def test_key_dir_attribute_set(self):
        self.assertEqual(self.x.key_dir, self.key_dir)

    def test_keyring_attribute_is_keyring(self):
        self.assertIsInstance(self.x.key_ring, keyring.KeyRing)

    def test_keyring_keydir_attribute(self):
        self.assertEqual(self.x.key_dir, self.x.key_ring.home)

    def test_key_finder_attribute_set(self):
        self.assertIsInstance(self.x.key_finder, keyfinder.KeyFinder)

    def test_key_finder_called_with_keyring(self):
        self.assertEqual(self.x.key_ring, self.x.key_finder.key_ring)

    def test_set_method_sets_keydir(self):
        self.x.set(self.alt_key_dir)
        self.assertEqual(self.x.key_dir, self.alt_key_dir)

    def test_set_method_sets_keyring_dir(self):
        sub = self.x.key_ring.set = MagicMock()
        self.x.set(self.alt_key_dir)
        sub.assert_called_with(self.alt_key_dir)

    @patch('gpg.gpgclient.encrypter.Encrypter')
    def test_encrypt_method_calls_keyfinder_get_fingerprint(self, mocked):
        sub = self.x.key_finder.get_fingerprint_by_keyid = MagicMock()
        result = self.x.encrypt(self.message, self.key_id)
        sub.assert_called_with(self.key_id)

    def test_encrypt_method_returns_none_if_fingerprint_is_none(self):
        sub = self.x.key_finder.get_fingerprint_by_keyid = MagicMock(return_value=None)
        result = self.x.encrypt(self.message, self.key_id)
        self.assertIsNone(result)

    @patch('gpg.gpgclient.encrypter.Encrypter')
    def test_encrypt_method_instantiates_encrypter_on_valid_input(self, mocked):
        result = self.x.encrypt(self.message, self.valid_keyid)
        self.assertTrue(mocked.called)

    @patch('gpg.gpgclient.encrypter.Encrypter.execute')
    def test_encrypt_method_calls_encrypter_execute_on_valid_input(self, mocked):
        result = self.x.encrypt(self.message, self.valid_keyid)
        self.assertTrue(mocked.called)

    @patch('gpg.gpgclient.encrypter.Encrypter.execute')
    def test_encrypt_method_returns_execute_result_on_valid_input(self, mocked):
        mocked.return_value = "Hello"
        result = self.x.encrypt(self.message, self.valid_keyid)
        self.assertEqual(result, mocked.return_value)

    @patch('gpg.gpgclient.decrypter.Decrypter')
    def test_decrypt_method_instantiates_decrypter(self, mocked):
        result = self.x.decrypt(self.message, self.passphrase)
        self.assertTrue(mocked.called)

    @patch('gpg.gpgclient.decrypter.Decrypter.execute')
    def test_decrypt_method_calls_decrypter_execute(self, mocked):
        result = self.x.decrypt(self.message, self.passphrase)
        mocked.assert_called_with(self.message, self.passphrase)

    @patch('gpg.gpgclient.decrypter.Decrypter.execute')
    def test_decrypt_method_returns_result_decrypter_execute(self, mocked):
        mocked.return_value = 'hello'
        result = self.x.decrypt(self.message, self.passphrase)
        self.assertEqual(result, mocked.return_value)

    def test_export_method_returns_pubkey_on_valid_input(self):
        result = self.x.export_key(self.valid_keyid)
        pub_key_string = '-----BEGIN PGP PUBLIC KEY BLOCK-----'
        self.assertIn(pub_key_string, result)

    def test_export_method_returns_empty_string_on_invalid_keyid(self):
        result = self.x.export_key('xxx')
        self.assertEqual(result, '')

    def test_import_method_returns_result_object(self):
        bad_key = 'xxxx'
        result = self.x.import_key(bad_key)
        self.assertEqual(result.imported, 0)

    @patch('gpg.gpgclient.signer.Signer')
    def test_sign_method_instantiates_signer(self, mocked):
        self.message = "Hello world."
        result = self.x.sign(self.message, self.valid_key_fingerprint, self.passphrase, detach=False)
        self.assertTrue(mocked.called)

    @patch('gpg.gpgclient.signer.Signer.execute')
    def test_sign_method_calls_execute_on_signer(self, mocked):
        self.message = "Hello world."
        result = self.x.sign(self.message, self.valid_key_fingerprint, self.passphrase, detach=False)
        self.assertTrue(mocked.called)

    @patch('gpg.gpgclient.signer.Signer.execute')
    def test_sign_method_returns_result_of_execute(self, mocked):
        mocked.return_value = 'xxx666'
        self.message = "Hello world."
        result = self.x.sign(self.message, self.valid_key_fingerprint, self.passphrase, detach=False)
        self.assertEqual(result, mocked.return_value)

    @patch('gpg.gpgclient.verifier.Verifier')
    def test_verify_method_instantiates_verifier(self, target):
        msg = 'hello'
        self.x.verify(msg)
        self.assertTrue(target.called)

    @patch('gpg.gpgclient.verifier.Verifier.execute')
    def test_method_calls_execute_on_verifier(self, mocked):
        self.message = "Hello world."
        result = self.x.verify(self.message)
        mocked.assert_called_with(self.message)

    @patch('gpg.gpgclient.verifier.Verifier.execute')
    def test_sign_method_returns_result(self, mocked):
        mocked.return_value = '123'
        self.message = "Hello world."
        result = self.x.verify(self.message)
        self.assertEqual(result, mocked.return_value)
