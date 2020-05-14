"""
test_keyfinder.py

Test suite for the KeyFinder module and class

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""
import dptools.gpg.tests.basegpgtestclass
from dptools.gpg.helpers import keyfinder
from dptools.gpg.agents import keyring
from dptools.gpg.tests.data import common


class TestKeyFinderClass(dptools.gpg.tests.basegpgtestclass.BaseGPGTestClass):

    def setUp(self):
        self.mal = {'type': 'pub',
                    'trust': 'u',
                    'length': '2048',
                    'algo': '1',
                    'keyid': common.current_key_keyid_keys_dir_ring,
                    'date': '1523719389',
                    'expires': '1838174400',
                    'dummy': '',
                    'ownertrust': 'u',
                    'sig': '',
                    'uids': ['alice (in wonderland) <alice@email.com>'],
                    'sigs': [],
                    'subkeys': [['', 'e', '']],
                    'fingerprint': common.current_key_fingerprint_keys_dir_ring}
        self.valid_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.valid_secret_fingerprint = common.current_key_fingerprint_keys_dir_ring
        self.valid_secret_keyid = common.current_key_keyid_keys_dir_ring
        self.keydir = self.key_dir_path
        self.key_ring = keyring.KeyRing(self.keydir)
        self.key_finder = keyfinder.KeyFinder(self.key_ring)

    def test_instance(self):
        self.assertIsInstance(self.key_finder, keyfinder.KeyFinder)

    def test_has_key_ring_attribute(self):
        name = 'key_ring'
        check = hasattr(self.key_finder, name)
        self.assertTrue(check)

    def test_key_ring_attribute_set(self):
        self.assertEqual(self.key_ring, self.key_finder.key_ring)

    # FIND METHOD

    def test_has_find_method(self):
        name = 'find'
        check = hasattr(self.key_finder, name)
        self.assertTrue(check)

    def test_find_method_valid_not_none(self):
        result = self.key_finder.find(self.valid_fingerprint)
        self.assertIsNotNone(result)

    def test_find_method_returns_key_dict_with_valid_fingerprint(self):
        result = self.key_finder.find(self.valid_fingerprint)
        self.assertEqual(result['fingerprint'], self.mal['fingerprint'])

    def test_find_method_returns_key_dict_with_valid_key_id(self):
        result = self.key_finder.find(self.mal['keyid'])
        self.assertEqual(result['keyid'], self.mal['keyid'])

    def test_find_method_returns_none_on_invalid(self):
        result = self.key_finder.find('xxx6666')
        self.assertIsNone(result)

    # FIND SECRET METHOD
    def test_has_find_secret_method(self):
        name = 'find_secret'
        check = hasattr(self.key_finder, name)
        self.assertTrue(check)

    def test_find_secret_method_valid_not_none(self):
        result = self.key_finder.find_secret(self.valid_secret_fingerprint)
        self.assertIsNotNone(result)

    def test_find_secret_method_valid_fingerprint_returns_secret(self):
        result = self.key_finder.find_secret(self.valid_secret_fingerprint)
        self.assertEqual(result['type'], 'sec')

    def test_find_secret_method_valid_keyid_returns_secret(self):
        result = self.key_finder.find_secret(self.valid_secret_keyid)
        self.assertEqual(result['type'], 'sec')

    def test_find_secret_method_returns_none_on_invalid(self):
        result = self.key_finder.find_secret('xxx6666')
        self.assertIsNone(result)

    # Key List Loop Method
    def test_has_search_list_method(self):
        name = '_search_list'
        check = hasattr(self.key_finder, name)
        self.assertTrue(check)

    def test_search_list_valid_fingerprint(self):
        key_dict = self.key_finder.find(self.valid_fingerprint)
        key_list = [key_dict]
        result = self.key_finder._search_list(key_list, self.valid_fingerprint)
        self.assertEqual(key_dict, result)

    def test_search_list_valid_secret_fingerprint(self):
        key_dict = self.key_finder.find(self.valid_secret_fingerprint)
        key_list = [key_dict]
        result = self.key_finder._search_list(key_list, self.valid_secret_keyid)
        self.assertEqual(key_dict, result)

    def test_search_list_not_valid_returns_none(self):
        key_dict = self.key_finder.find(self.valid_fingerprint)
        key_list = [key_dict]
        result = self.key_finder._search_list(key_list, 'xxxx')
        self.assertIsNone(result)

    # Get Fingerprint By KeyID
    def test_get_fingerprint_by_keyid_returns_valid(self):
        keyid = self.valid_secret_keyid
        result = self.key_finder.get_fingerprint_by_keyid(keyid)
        self.assertEqual(result, self.valid_fingerprint)

    def test_get_fingerprint_by_keyid_returns_none_with_invalid(self):
        keyid = 'xxx666'
        result = self.key_finder.get_fingerprint_by_keyid(keyid)
        self.assertIsNone(result)