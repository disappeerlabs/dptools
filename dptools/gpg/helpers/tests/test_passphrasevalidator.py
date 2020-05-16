"""
test_passphrasevalidator.py

Test suite for PassphraseValidator module.
Takes passphrase, homedir and host key id, checks signs and verify with passphrase.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.helpers import passphrasevalidator
from dptools.gpg.agents import signer, verifier


@unittest.skipIf(*mark.slow)
class TestPassphraseValidatorBasicsSlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_master = helpers.SetUpKeys()
        cls.key_master.set_up_alice()

    def setUp(self):
        self.maxDiff = None
        self.home_dir = self.key_master.alice_dir_path
        self.host_key_id = self.key_master.alice_key['keyid']
        self.passphrase = 'passphrase'
        self.msg = 'hello world'
        self.x = passphrasevalidator.PassphraseValidator(self.home_dir, self.host_key_id, self.passphrase)

    def test_signer_import(self):
        self.assertEqual(signer, passphrasevalidator.signer)

    def test_verifier_import(self):
        self.assertEqual(verifier, passphrasevalidator.verifier)

    def test_instance(self):
        self.assertIsInstance(self.x, passphrasevalidator.PassphraseValidator)

    def test_home_dir_attr(self):
        self.assertEqual(self.home_dir, self.x.home_dir)

    def test_host_key_id_attr(self):
        self.assertEqual(self.host_key_id, self.x.host_key_id)

    def test_passphrase_attr(self):
        self.assertEqual(self.passphrase, self.x.passphrase)

    def test_msg_attr(self):
        self.assertEqual(self.x.msg, self.msg)

    def test_sign_method_returns_valid_sig_of_message(self):
        sig_result = self.x.sign()
        verify_agent = verifier.Verifier(self.home_dir)
        result = verify_agent.execute(str(sig_result))
        self.assertIs(result.valid, True)

    def test_verify_method_returns_result_of_verification(self):
        sign_agent = signer.Signer(self.home_dir)
        target = sign_agent.execute(self.msg, self.host_key_id, self.passphrase)
        result = self.x.verify(str(target))
        self.assertTrue(result.valid)

    def test_validate_returns_verify_valid_result(self):
        result = self.x.validate()
        self.assertIs(result, True)

    def test_validate_sets_result_attr(self):
        result = self.x.validate()
        self.assertIsNotNone(self.x.result)

    def test_result_attr(self):
        self.assertIsNone(self.x.result)

    def test_get_error_msg_returns_error_msg_from_result(self):
        class MockResult:
            stderr = 'hello'
        self.x.result = MockResult()
        result = self.x.get_error_msg()
        self.assertEqual(result, self.x.result.stderr)

    def test_get_error_msg_returns_none_when_result_not_set(self):
        class MockResult:
            mmm = 'xxxx'
        self.x.result = MockResult()
        result = self.x.get_error_msg()
        self.assertIsNone(result)


@unittest.skipIf(*mark.slow)
class TestPassphraseValidatorSlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_master = helpers.SetUpKeys()
        cls.key_master.set_up_alice()

    def setUp(self):
        self.maxDiff = None
        self.home_dir = self.key_master.alice_dir_path
        self.host_key_id = self.key_master.alice_key['keyid']
        self.passphrase = 'passphrase'
        self.msg = 'hello world'

    def test_validate_returns_verify_false_on_invalid_result(self):
        invalid_x = passphrasevalidator.PassphraseValidator(self.home_dir, self.host_key_id, '')
        sig = invalid_x.sign()
        self.assertIsNone(sig.status)
