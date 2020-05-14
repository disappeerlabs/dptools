"""
test_passphrasevalidator.py

Test suite for PassphraseValidator module.
Takes passphrase, homedir and host key id, checks signs and verify with passphrase.

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.gpg.helpers import passphrasevalidator
# from dptools.models import gpgdatacontext
from dptools.gpg.agents import signer
from dptools.gpg.agents import verifier
from dptools.gpg.tests.data import common
from dptools.gpg.tests import basegpgtestclass


class TestImports(unittest.TestCase):

    def test_signer(self):
        self.assertEqual(signer, passphrasevalidator.signer)

    def test_verifier(self):
        self.assertEqual(verifier, passphrasevalidator.verifier)


class TestClassBasics(basegpgtestclass.BaseGPGTestClass):

    def setUp(self):
        self.maxDiff = None
        self.test_key_dir = self.key_dir_path
        self.home_dir = self.key_dir_path
        self.host_key_id = common.current_key_keyid_keys_dir_ring
        self.passphrase = 'passphrase'
        self.msg = 'hello world'
        self.x = passphrasevalidator.PassphraseValidator(self.home_dir, self.host_key_id, self.passphrase)

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

    @unittest.skip("Getting unexpected behavior from gnupg, requires investigation")
    def test_validate_returns_verify_false_on_invalid_result(self):
        invalid_x = passphrasevalidator.PassphraseValidator(self.home_dir, self.host_key_id, '')
        sig = invalid_x.sign()
        print(sig.stderr)
        print(sig.status)
        # o = invalid_x.validate()
        # print(o)
        # assert False

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




