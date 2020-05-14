"""
basegpgtestclass.py

> ENTER DESCRIPTION HERE

Copyright (C) 2020 Disappeer Labs
License: GPLv3
"""
import os
import unittest

from dptools.gpg.tests.data import keys, altkeys


class BaseGPGTestClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key_dir_path = os.path.dirname(keys.__file__)
        cls.alt_key_dir_path = os.path.dirname(altkeys.__file__)

import tempfile
import gnupg
from dptools.gpg.tests.helpers import alice_key_vals_dict, bob_key_vals_dict, key_reference_dict, create_key_input_dict


class SetUpKeys:

    def __init__(self):
        self.temp_dir_alice = tempfile.TemporaryDirectory()
        self.alice_dir_path = self.temp_dir_alice.name
        self.temp_dir_bob = tempfile.TemporaryDirectory()
        self.bob_dir_path = self.temp_dir_bob.name

    def set_up_alice(self):
        print("Setting up Alice")
        self.alice_gpg = gnupg.GPG(gnupghome=self.alice_dir_path)
        self.alice_input_data = self.alice_gpg.gen_key_input(**create_key_input_dict(key_reference_dict, alice_key_vals_dict))
        self.alice_gpg.gen_key(self.alice_input_data)
        self.alice_key = self.alice_gpg.list_keys()[0]
        self.alice_export = self.alice_gpg.export_keys(self.alice_key['keyid'])

    def set_up_bob(self):
        print("Setting up Bob")
        self.bob_gpg = gnupg.GPG(gnupghome=self.bob_dir_path)
        self.bob_input_data = self.bob_gpg.gen_key_input(**create_key_input_dict(key_reference_dict, bob_key_vals_dict))
        self.bob_gpg.gen_key(self.bob_input_data)
        self.bob_key = self.bob_gpg.list_keys()[0]
        self.bob_export = self.bob_gpg.export_keys(self.bob_key['keyid'])

    def set_up_alice_and_bob(self):
        self.set_up_alice()
        self.set_up_bob()
        self.alice_gpg.import_keys(str(self.bob_export))
        self.bob_gpg.import_keys(str(self.alice_export))

    def __del__(self):
        self.temp_dir_alice.cleanup()
        self.temp_dir_bob.cleanup()
