"""
test_keylistformatter.py

Test suite for KeyListFormatter module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.tests import mark
from dptools.gpg.tests import helpers
from dptools.gpg.helpers import keylistformatter
from dptools.gpg.agents import keyring


@unittest.skipIf(*mark.slow)
class TestKeyListFormatterBasics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_master = helpers.SetUpKeys()
        cls.key_master.set_up_alice()
        cls.fingerprint = cls.key_master.alice_key['fingerprint']
        cls.keyid = cls.key_master.alice_key['keyid']

    def setUp(self):
        self.keydir = self.key_master.alice_dir_path
        self.key_ring = keyring.KeyRing(self.keydir)
        self.key_list = self.key_ring.get_raw_key_list()

        self.name = helpers.alice_key_vals_dict['Name']
        self.email = '<' + helpers.alice_key_vals_dict['Email'] + '>'
        self.keyid = self.key_master.alice_key['keyid']

        self.user_key_uid_string = self.key_master.alice_key['uids'][0]
        self.key_uid_string = self.key_list[0]['uids'][0]
        self.x = keylistformatter.KeyListFormatter()

    def test_instance(self):
        self.assertIsInstance(self.x, keylistformatter.KeyListFormatter)

    def test_format_method_attribute(self):
        name = 'format'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_format_method_takes_list_arg(self):
        result = self.x.format(self.key_list)
        self.assertIsNotNone(result)

    def test_process_key_uid_string_method_attribute(self):
        name = 'process_key_uid'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_process_key_uid_string_result_is_not_none(self):
        result = self.x.process_key_uid(self.key_uid_string)
        self.assertIsNotNone(result)

    def test_process_key_uid_string_returns_packed_tuple(self):
        result = self.x.process_key_uid(self.key_uid_string)
        target_string = self.user_key_uid_string
        split = target_string.split()
        check = (split[0], split[-1])
        self.assertEqual(result, check)

    def test_create_userid_and_keyid_tuple_attribute(self):
        name = 'create_userid_and_keyid_tuple_list'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_create_userid_and_keyid_tuple_method_takes_raw_list(self):
        result = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        self.assertIsNotNone(result)

    def test_create_userid_and_key_id_returns_tuple(self):
        userid = self.user_key_uid_string
        keyid = self.keyid
        target = (userid, keyid)
        result = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        self.assertIn(target, result)

    def test_process_key_dropdown_strings_attribute(self):
        name = 'process_key_dropdown_list_strings'
        check = hasattr(self.x, name)
        self.assertTrue(check)

    def test_process_key_dropdown_strings_method_result(self):
        spacer = ', '
        target_string = self.name + spacer + self.email + spacer + self.keyid
        interim = self.x.create_userid_and_keyid_tuple_list(self.key_list)
        result = self.x.process_key_dropdown_list_strings(interim)
        self.assertIn(target_string, result)

    def test_format_result(self):
        target = [self.name + ', ' + self.email + ', ' + self.keyid]
        result = self.x.format(self.key_list)
        for item in target:
            self.assertIn(item, result)
