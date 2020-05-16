"""
test_tempdetachedverifier.py

Test suite for TempDetachedVerifier class object and module.
Object should take gpg_pub_key and sig_dict as input.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
import json
import copy
import tempfile
from unittest.mock import MagicMock
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.helpers import tempdetachedverifier, tempkeyring
from dptools.gpg.agents import detachedverifier, keyring, signer


class TestTempDetachedVerifierBasics(unittest.TestCase):

    def setUp(self):
        self.mock_pub_key = ''
        self.mock_sig_dict = {}
        self.x = tempdetachedverifier.TempDetachedVerifier(self.mock_pub_key, self.mock_sig_dict)

    def test_tempkeyring_import(self):
        self.assertEqual(tempkeyring, tempdetachedverifier.tempkeyring)

    def test_detachedverifier_import(self):
        self.assertEqual(detachedverifier, tempdetachedverifier.detachedverifier)

    def test_tempfile_import(self):
        self.assertEqual(tempfile, tempdetachedverifier.tempfile)

    def test_instance(self):
        self.assertIsInstance(self.x, tempdetachedverifier.TempDetachedVerifier)

    def test_instance_tempkeyring(self):
        self.assertIsInstance(self.x, tempkeyring.TempKeyRing)

    def test_parent_attribute_not_none(self):
        self.assertIsNotNone(self.x.temp_dir)

    def test_gpg_pub_key_attribute_set(self):
        self.assertEqual(self.x.gpg_pub_key, '')

    def test_sig_dict_attribute_set(self):
        self.assertEqual(self.x.sig_dict, self.mock_sig_dict)

    def test_valid_attribute_set(self):
        check = hasattr(self.x, 'valid')
        self.assertTrue(check)

    def test_detached_verifier_attribute_is_detached_verifier(self):
        self.assertIsInstance(self.x.detached_verifier, detachedverifier.DetachedVerifier)
        self.assertEqual(self.x.detached_verifier.home, self.x.temp_dir_name)


@unittest.skipIf(*mark.slow)
class TestTempDetachedVerifierSlow(unittest.TestCase):

    @classmethod
    def build_mock_sig_dict(cls, data_dict):
        encoded_data_dict = json.dumps(data_dict)
        key_dir = cls.key_master.alice_dir_path

        sign_executer = signer.Signer(key_dir)
        result = sign_executer.execute(encoded_data_dict, None, 'passphrase', detach=True)
        final_dict = dict(sig=str(result), data=encoded_data_dict)
        return final_dict, result.fingerprint

    @classmethod
    def get_gpg_pubkey(cls, fingerprint):
        key_dir = cls.key_master.alice_dir_path
        key_ring = keyring.KeyRing(key_dir)
        result = key_ring.export_key(fingerprint)
        return result

    @classmethod
    def setUpClass(cls):
        cls.key_master = helpers.SetUpKeys()
        cls.key_master.set_up_alice()
        cls.data_dict = dict(desc='Hello World')
        cls.sig_dict, fingerprint = cls.build_mock_sig_dict(cls.data_dict)
        cls.gpg_pub_key = cls.get_gpg_pubkey(fingerprint)
        cls.valid_obj = tempdetachedverifier.TempDetachedVerifier(cls.gpg_pub_key, cls.sig_dict)

    def setUp(self):
        self.x = copy.deepcopy(self.valid_obj)

    def test_error_attribute_set_none(self):
        self.assertIsNone(self.x.error)

    def test_set_error_method_sets_error_and_valid(self):
        msg = 'Error Message'
        self.x.set_error(msg)
        self.assertEqual(self.x.error, msg)
        self.assertIs(self.x.valid, False)

    def test_is_key_valid_returns_false_sets_error_and_valid_false_on_bad_key(self):
        self.x.gpg_pub_key = 'xxx'
        result = self.x.is_key_valid()
        self.assertIsNotNone(self.x.error)
        self.assertIs(self.x.valid, False)
        self.assertIs(result, False)

    def test_is_key_valid_returns_true_on_valid(self):
        result = self.x.is_key_valid()
        self.assertIs(result, True)

    def test_is_sig_dict_valid_returns_true_on_valid_sig_dict(self):
        result = self.x.is_sig_dict_valid()
        self.assertIs(result, True)

    def test_is_sig_dict_valid_returns_false_sets_error_on_invalid_sig_dict(self):
        self.x.sig_dict = 'xxx'
        result = self.x.is_sig_dict_valid()
        self.assertIs(result, False)
        self.assertIsNotNone(self.x.error)

    def test_verify_sig_sets_error_on_invalid_sig(self):
        self.x.sig_dict = dict(sig='xxx', data='yyy')
        result = self.x.verify_sig()
        self.assertIs(result, False)
        self.assertIs(self.x.valid, False)

    def test_verify_sig_returns_valid_on_valid_sig(self):
        self.x.is_key_valid()
        result = self.x.verify_sig()
        self.assertIs(result, True)
        self.assertIs(self.x.valid, True)

    def test_run_method_calls_is_key_valid(self):
        target = self.x.is_key_valid = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_method_calls_is_sig_dict_valid(self):
        target = self.x.is_sig_dict_valid = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_method_calls_verify_sig(self):
        target = self.x.verify_sig = MagicMock()
        self.x.run()
        target.assert_called_with()

    def test_run_does_not_call_is_sig_valid_if_key_not_valid(self):
        self.x.gpg_pub_key = 'xxx'
        target = self.x.is_sig_dict_valid = MagicMock()
        self.x.run()
        self.assertFalse(target.called)

    def test_run_does_not_call_verify_if_sig_dict_not_valid(self):
        self.x.sig_dict = 'xxx'
        target = self.x.verify_sig = MagicMock()
        self.x.run()
        self.assertFalse(target.called)

    def test_run_called_by_init(self):
        self.assertIsNotNone(self.x.valid)
