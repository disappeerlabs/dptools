"""
test_keylistformatter.py

Test suite for KeyListFormatter module and class

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""

import unittest
from dptools.gpg.helpers import keylistformatter
from dptools.gpg.agents import keyring
from dptools.gpg.tests.data import common, keys
from dptools.tests import basetestclass

# key_dir = 'tests/data/keys'

# user_name = 'mal'
# user_email = '<mallory@none.com>'
# user_keyid = common.current_key_keyid_keys_dir_ring
# user_key_uid_string = 'alice (in wonderland) <alice@email.com>'
#
# key_ring = keyring.KeyRing(key_dir)
# raw_key_list = key_ring.get_raw_key_list()


class TestKeyListFormatterBasics(basetestclass.BaseTestClass):

    def setUp(self):
        self.key_dir = self.key_dir_path
        self.key_ring = keyring.KeyRing(self.key_dir)
        self.raw_key_list = self.key_ring.get_raw_key_list()
        self.key_list = self.raw_key_list
        self.name = common.current_key_user_name
        self.email = common.current_key_user_email
        self.keyid = common.current_key_keyid_keys_dir_ring
        self.user_key_uid_string = common.current_key_uuid_raw_string_value
        self.keyid = common.current_key_keyid_keys_dir_ring
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
